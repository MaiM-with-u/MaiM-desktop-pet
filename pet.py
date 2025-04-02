from PyQt5.QtWidgets import QApplication, QLabel, QWidget,QMainWindow
from PyQt5.QtCore import Qt, QPoint,QTimer
from PyQt5.QtGui import QPixmap
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

        #气泡相关
        self.bubble = SpeechBubble(self)
        self.bubble.hide()


        # 拖拽相关变量
        self.drag_start_position = None

    
    #鼠标按下
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    #鼠标移动
    def mouseMoveEvent(self, event):
        """鼠标移动事件"""
        if event.buttons() == Qt.LeftButton and self.drag_start_position is not None:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()
    
    #鼠标释放
    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = None
            event.accept()

    #鼠标双击
    def mouseDoubleClickEvent(self, event):
        asyncio.run(chat_util.easy_to_send("你好"))

    #调用气泡显示的方法
    def show_message(self, text):
        """公开方法：显示气泡消息"""
        self.bubble.show_message(text)
        QTimer.singleShot(2000, self.bubble.fade_out) 


chat_pet = DesktopPet()
