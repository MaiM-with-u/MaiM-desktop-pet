from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMainWindow,QMenu,QSystemTrayIcon
from PyQt5.QtCore import Qt, QPoint,QTimer,pyqtSignal,QThread
from PyQt5.QtGui import QPixmap,QCursor,QIcon
from bubble import SpeechBubble
from util import chat_util,logger
import asyncio
import sys
import time
from qasync import asyncSlot

app = QApplication(sys.argv)

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_tray_icon()
        #气泡相关
        self.bubble = SpeechBubble(self)
        self.bubble.hide()

        self._move_worker = None  # 工作线程引用

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
        y = screen_geo.height() - self.height() - 20  # 下边距20px
        self.move(x, y)

    def mousePressEvent(self, event):
        """鼠标按下时创建工作线程"""
        if event.button() == Qt.LeftButton:
            # 计算初始偏移量(光标位置与窗口左上角的差值)
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            
            # 创建并启动工作线程
            self._move_worker = MoveWorker(self.drag_start_position)
            self._move_worker.position_changed.connect(self._on_position_changed)
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
        """接收工作线程发来的新位置并更新窗口"""
        self.move(pos)  # 主线程执行实际的窗口移动

    def mouseDoubleClickEvent(self, event):
        asyncio.run(chat_util.easy_to_send("你好"))

    #调用气泡显示的方法
    def show_message(self, text):
        """公开方法：显示气泡消息"""
        self.bubble.show_message(text)
        QTimer.singleShot(2000, self.bubble.fade_out) 

    def init_tray_icon(self):
        """初始化系统托盘图标（可选）"""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("./img/maim.png"))  # 托盘图标
        self.tray_icon.setToolTip("桌面宠物")
        
        # 托盘菜单
        tray_menu = QMenu()
        show_action = tray_menu.addAction("显示宠物")
        show_action.triggered.connect(self.show_pet)
        exit_action = tray_menu.addAction("退出")
        exit_action.triggered.connect(QApplication.quit)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def contextMenuEvent(self, event):
        """右键菜单"""
        menu = QMenu(self)
        
        # 添加菜单项
        hide_action = menu.addAction("隐藏宠物")
        hide_action.triggered.connect(self.hide_pet)
        
        show_action = menu.addAction("显示宠物")
        show_action.triggered.connect(self.show_pet)
        
        exit_action = menu.addAction("退出")
        exit_action.triggered.connect(QApplication.quit)
        
        menu.exec_(event.globalPos())

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



class MoveWorker(QThread):
    position_changed = pyqtSignal(QPoint)  # 定义信号，用于传递新位置
    
    def __init__(self, start_pos):
        super().__init__()
        self.start_pos = start_pos  # 存储拖动起始偏移量
        self._active = True  # 线程运行状态标志
    
    def run(self):
        """线程主循环"""
        while self._active:
            current_pos = QCursor.pos()  # 获取当前光标位置
            new_pos = current_pos - self.start_pos  # 计算新窗口位置
            self.position_changed.emit(new_pos)  # 发送信号
            self.msleep(16)  # 控制更新频率(~60fps)
    
    def stop(self):
        """安全停止线程"""
        self._active = False


chat_pet = DesktopPet()
