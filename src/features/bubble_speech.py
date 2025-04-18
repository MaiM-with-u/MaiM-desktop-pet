# views/bubble.py
from PyQt5.QtWidgets import QLabel,QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint,QSize,QRect
from PyQt5.QtGui import QPainter, QColor, QFont,QPainterPath


class SpeechBubble(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignCenter)
        
        # 可以修改这些属性自定义外观
        self.bg_color = QColor(240, 248, 255)  # 爱丽丝蓝
        self.text_color = QColor(70, 70, 70)   # 深灰色
        self.setFont(QFont("Arial", 12, QFont.Bold))
        self.corner_radius = 10
        self.arrow_height = 10
        self.follow_offset = QPoint(0, -30)  # 气泡相对于主体的偏移量
        
        # 字体设置
        self.setFont(QFont("Microsoft YaHei", 12))
       
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆角矩形主体
        body_rect = self.rect().adjusted(0, 0, 0, -self.arrow_height)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(body_rect, self.corner_radius, self.corner_radius)
        
        # 绘制底部箭头
        path = QPainterPath()
        arrow_width = 20
        center_x = self.width() // 2
        path.moveTo(center_x - arrow_width//2, body_rect.height())
        path.lineTo(center_x, self.height())
        path.lineTo(center_x + arrow_width//2, body_rect.height())
        painter.drawPath(path)
        
        # 绘制文字
        painter.setPen(self.text_color)
        painter.drawText(body_rect, Qt.AlignCenter | Qt.TextWordWrap, self.text())

    def calculate_bubble_size(self, text):
        metrics = self.fontMetrics()
        max_width = 300  # 气泡最大宽度
        min_width = 150  # 气泡最小宽度
        
        # 计算文本所需宽度
        text_width = metrics.width(text)
        # 计算自动换行后的实际需要宽度
        if text_width > max_width:
            actual_width = max_width
            # 计算换行后的高度
            text_rect = metrics.boundingRect(QRect(0, 0, max_width, 0),
                                            Qt.TextWordWrap, text)
            height = text_rect.height() + 30
        else:
            actual_width = max(min_width, text_width + 20)
            height = metrics.height() + 20
        
        return QSize(actual_width, height)

    def show_message(self, text):
        """显示气泡消息"""

        self.setText(text)
        size = self.calculate_bubble_size(text)
        self.resize(size)
        
        # 计算气泡位置（位于父控件上方居中）
        if self.parent():
            parent_rect = self.parent().geometry()
            x = parent_rect.center().x() - self.width() // 2
            y = parent_rect.top() - self.height() + self.follow_offset.y()
            self.move(x, y)
        
        self.show()
        
    def fade_out(self):
        
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(500)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        self.hide()
        anim.start()

    def update_position(self):
        if not self.parent() or not self.isVisible():
            return
        
        parent_rect = self.parent().geometry()
        screen_geo = QApplication.primaryScreen().availableGeometry()
        
        # 计算理想位置
        ideal_x = parent_rect.center().x() - self.width() // 2
        ideal_y = parent_rect.top() - self.height() + self.follow_offset.y()
        
        # 边界约束
        new_x = max(screen_geo.left() + 5,  # 左边距5px
                min(ideal_x, 
                    screen_geo.right() - self.width() - 5))  # 右边距5px
        
        # 如果上方空间不足，改为显示在下方
        if ideal_y < screen_geo.top():
            new_y = parent_rect.bottom() - self.follow_offset.y()
            self.arrow_height = -abs(self.arrow_height)  # 箭头朝下
        else:
            new_y = ideal_y
            self.arrow_height = abs(self.arrow_height)  # 箭头朝上
        
        self.move(new_x, new_y)
        self.update()  # 触发重绘以更新箭头方向

bubble = SpeechBubble()