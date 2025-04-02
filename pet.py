from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMainWindow
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
from bubble import SpeechBubble
from util import chat_util
import asyncio
import sys

app = QApplication(sys.argv)

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()
        
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


        # 拖拽相关变量
        self.drag_start_position = None

        #气泡相关
        self.bubble = SpeechBubble(self)
        self.bubble.hide()
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position is not None:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()
        if self.bubble.isVisible():
            self.bubble.update_position()
    
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = None
            event.accept()

    def show_message(self, text, duration=2):
        """公开方法：显示气泡消息"""
        self.bubble.show_message(text, duration)

    def mouseDoubleClickEvent(self, event):
        asyncio.run(chat_util.easy_to_send("你好"))

    def sync_bubble_position(self):
        """同步气泡位置"""
        if self.bubble.isVisible():
            self.bubble.update_position()

chat_pet = DesktopPet()
