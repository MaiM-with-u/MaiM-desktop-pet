from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMenu,QSystemTrayIcon
from PyQt5.QtCore import Qt,QTimer,QThread,QPropertyAnimation,QEasingCurve,QSize
from PyQt5.QtGui import QPixmap,QCursor,QIcon

from src.core.chat import chat_util  # noqa: F401
from src.core.signals import signals_bus

from src.features.bubble_menu import BubbleMenu
from src.features.bubble_speech import SpeechBubble
from src.features.bubble_input import BubbleInput  # 新增导入
from src.features.ScreenshotSelector import ScreenshotSelector

from src.util.logger import logger  # noqa: F401
from src.util.image_util import pixmap_to_base64

from config import Config

import asyncio
import sys
from datetime import datetime  # 正确导入方式 # noqa: F401
import platform 

config = Config()

app = QApplication(sys.argv)

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_tray_icon()

        #麦麦气泡初始化
        self.bubble = SpeechBubble(parent=self)
        self.bubble.hide()

        #右键菜单初始化
        self.bubble_menu = BubbleMenu()
        # self.bubble_menu.hide()

        #输入菜单初始化
        self.bubble_input = BubbleInput(parent=self, on_send=self.handle_user_input)
        self.bubble_input.hide()

        self._move_worker = None  # 工作线程引用

        # 定时器（未启用）
        # self.thinktimer = QTimer(self)
        # self.thinktimer.timeout.connect(self._on_timer_triggered)  # 连接信号
        # self.thinktimer.start(60 * 1000)  # 60秒（单位：毫秒）

        signals_bus.message_received.connect(self.show_message)

        self.screenshot_selector = None

        if config.hide_console:
            self.show_message("终端藏在托盘栏咯，进入托盘栏打开叭")

        
    #主窗口初始化相关
    def init_ui(self):

        # 设置窗口属性
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # 无边框
            Qt.WindowStaysOnTopHint |  # 始终在最前
            Qt.SubWindow              # 子窗口
        )
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景
        self.setFixedSize(400, 600)
        
        # 加载图片
        self.pet_image = QLabel(self)
        pixmap = QPixmap("./img/small_maimai.png")  # 替换为你的图片路径img/maimai.png
        self.pet_image.setPixmap(pixmap)
        self.pet_image.resize(pixmap.size())
        
        # 设置初始位置和大小
        screen_geo = QApplication.primaryScreen().availableGeometry()  # 获取可用屏幕区域（排除任务栏）
        x = screen_geo.width() - self.width() - 20  # 右边距20px
        y = screen_geo.height() - self.height() - 80  # 下边距20px
        self.move(x, y)

    def init_tray_icon(self):
        """初始化系统托盘图标（增加终端控制功能）"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./img/maim.png"))
        self.tray_icon.setToolTip("桌面宠物")
        
        # 获取终端窗口句柄（Windows专用）
        self.console_visible = True  # 默认终端可见
        if platform.system() == "Windows":
            import win32gui # noqa: E401
            self.console_window = win32gui.GetForegroundWindow()
        else:
            self.console_window = None
        
        # 托盘菜单（保持原有样式）
        tray_menu = QMenu()
        tray_menu.setStyleSheet("""
            QMenu {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                padding: 5px 20px;
                color: #333;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
                color: white;
            }
            QMenu::item:disabled {
                color: #999;
            }
        """)
        
        # 宠物控制
        show_action = tray_menu.addAction("显示宠物")
        show_action.triggered.connect(self.show_pet)
        
        # 终端控制按钮
        self.toggle_term_action = tray_menu.addAction("隐藏终端")  # 初始状态为隐藏终端
        self.toggle_term_action.triggered.connect(self.toggle_console)
        
        # 退出
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("退出")
        exit_action.triggered.connect(self.safe_quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.update_terminal_menu_state()
        if config.hide_console:
            self.hide_console()
        

    def toggle_console(self):
        """切换终端窗口的显示和隐藏状态"""
        if self.console_visible:
            self.hide_console()
        else:
            self.show_console()
        self.update_terminal_menu_state()

    def show_console(self):
        """显示终端窗口"""
        if platform.system() == "Windows":
            import win32gui, win32con  # noqa: E401
            win32gui.ShowWindow(self.console_window, win32con.SW_SHOW)
        else:
            print("\n[终端已显示 - 输入Ctrl+C退出]\n")
        self.console_visible = True
        self.update_terminal_menu_state()

    def hide_console(self):
        """隐藏终端窗口"""
        if platform.system() == "Windows":
            import win32gui, win32con # noqa: E401
            win32gui.ShowWindow(self.console_window, win32con.SW_HIDE)
        self.console_visible = False
        self.update_terminal_menu_state()

    def update_terminal_menu_state(self):
        """更新终端控制按钮的文本"""
        if self.console_visible:
            self.toggle_term_action.setText("隐藏终端")
        else:
            self.toggle_term_action.setText("显示终端")

    def safe_quit(self):
        """安全退出程序（恢复终端显示）"""
        if not self.console_visible:
            self.show_console()
        QApplication.quit()

    #移动相关线程
    def mousePressEvent(self, event):
        """鼠标按下时创建工作线程"""
        if event.button() == Qt.LeftButton:
            # 计算初始偏移量(光标位置与窗口左上角的差值)
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
        if event.button() == Qt.LeftButton and not self._move_worker:
            # 创建并启动工作线程
            self._move_worker = MoveWorker(self.drag_start_position,self)
            signals_bus.position_changed.connect(self._on_position_changed)
            self._move_worker.start()
            event.accept()
   
    def mouseReleaseEvent(self, event):
        """鼠标释放时停止工作线程"""
        if event.button() == Qt.LeftButton and self._move_worker:
            self._move_worker.stop()  # 设置停止标志
            self._move_worker.wait()  # 等待线程结束
            self._move_worker = None  # 清理引用
            self.drag_start_position = None
            event.accept()
    
    def _on_position_changed(self, pos):
        """
        窗口移动时更新输入气泡位置
        包含了所有子窗口的移动
        """
        self.move(pos)
        if self.bubble_input.isVisible():
            self.bubble_input.update_position()
        if self.bubble.isVisible():
            self.bubble.update_position()

    #鼠标双击逻辑
    def mouseDoubleClickEvent(self, event):
        asyncio.run(chat_util.easy_to_send("(这是一个类似于摸摸头的友善动作)","text"))

    #消息显示逻辑
    def show_message(self, text):
        """公开方法：显示气泡消息"""
        self.bubble.show_message(text)
        QTimer.singleShot(len(text)*1000, self.bubble.fade_out) 

    #基础桌宠行为
    def hide_pet(self):
        """隐藏宠物（图片 + 任务栏）"""
        self.hide()  # 隐藏窗口
        # 如果不需要托盘图标，可以完全隐藏：
        # self.setWindowFlags(self.windowFlags() | Qt.Tool)
        # self.show()  # 必须重新调用 show() 使 flags 生效

    def show_pet(self):
        """显示宠物"""
        self.show()  # 显示窗口
        # 恢复任务栏图标（如果需要）：
        # self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
        # self.show()

    #右键菜单
    def contextMenuEvent(self, event):
        if self._move_worker:
            self._move_worker.stop()
        menu = BubbleMenu(self)
        
        actions = [
            ("🐾 隐藏", self.hide),
            ("✏️ 聊聊天", self.show_chat_input),  
            ("📸 截图", self.start_screenshot),
            ("❌ 退出", QApplication.quit),
        ]

        for text, callback in actions:
            action = menu.addAction(text)
            action.triggered.connect(callback)

        menu.exec_(event.globalPos()) 

    def add_hover_animation(self, action):
        """为菜单项添加悬停动画"""
        animation = QPropertyAnimation(action, b"iconSize")
        animation.setDuration(200)
        animation.setEasingCurve(QEasingCurve.OutQuad)
        animation.setStartValue(QSize(16, 16))
        animation.setEndValue(QSize(20, 20))
        action.hovered.connect(animation.start)

    def show_chat_input(self):
        """显示输入气泡"""
        self.bubble_input.show()
        self.bubble_input.update_position()
        self.bubble_input.input_field.setFocus()

    def handle_user_input(self, text):
        """处理用户输入的回调函数"""
        print(f"收到用户输入: {text}")
        asyncio.run(chat_util.easy_to_send(str(text),"text"))
        # self.show_message(f"你说了: {text}")
        # asyncio.run(chat_util.process_input(text))

    def start_screenshot(self):
        """启动区域截图"""
        self.hide()  # 隐藏宠物避免干扰
        self.bubble.hide()

        # 创建选择器（需继承ScreenshotSelector）
        self.screenshot_selector = PetScreenshotSelector(self)
        self.screenshot_selector.show()

    def handle_screenshot(self, pixmap):
        """处理截图结果"""
        self.show()  # 重新显示宠物
        
        # 显示在气泡中
        self.bubble.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        
        base64_str = pixmap_to_base64(pixmap)
        asyncio.run(chat_util.easy_to_send(base64_str,"image"))
        # 保存文件

    #定时器（未启用）
    def _on_timer_triggered(self):
        """定时器触发时执行的函数"""
        print("60秒定时器触发！")
        # asyncio.run(chat_util.easy_to_send("你现在在想什么呢","text"))
        # 这里添加你的业务逻辑，例如：
        # self.check_updates()
        # self.auto_save()



# 自定义选择器（处理截图回调）
class PetScreenshotSelector(ScreenshotSelector):
    def __init__(self, pet):
        super().__init__()
        self.pet = pet
    
    def on_screenshot_captured(self, pixmap):
        self.pet.handle_screenshot(pixmap)

# 移动管理器

class MoveWorker(QThread):
    def __init__(self, start_pos, pet_widget):
        super().__init__()
        self.start_pos = start_pos  # 存储拖动起始偏移量
        self._active = True  # 线程运行状态标志
        self.pet_widget = pet_widget  # 桌宠控件

    def run(self):
        """线程主循环"""
        while self._active:
            # 检查桌宠是否是焦点目标
            if not self.pet_widget.isActiveWindow():
                self.stop()
                break

            current_pos = QCursor.pos()  # 获取当前光标位置
            new_pos = current_pos - self.start_pos  # 计算新窗口位置
            signals_bus.position_changed.emit(new_pos)  # 发送信号
            self.msleep(8)  # 控制更新频率(~120fps)

    def stop(self):
        """安全停止线程"""
        self._active = False


chat_pet = DesktopPet()
