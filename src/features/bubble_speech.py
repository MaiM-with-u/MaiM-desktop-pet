from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint, QSize, QRect, QSequentialAnimationGroup
from PyQt5.QtGui import QPainter, QColor, QFont, QPainterPath

class SpeechBubble(QLabel):
    _active_bubbles = []  # 类变量，保存所有活动气泡
    _vertical_spacing = 5  # 气泡之间的垂直间距
    
    def __init__(self, parent=None, bubble_type="received"):
        super().__init__(parent)
        self.setWindowFlags(Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)  # 改为左对齐
        
        self.bubble_type = bubble_type  # "received" 或 "sent"
        
        # 根据气泡类型设置不同样式
        if bubble_type == "received":
            self.bg_color = QColor(240, 248, 255)  # 爱丽丝蓝(接收气泡)
            self.follow_offset = QPoint(-100, -30)   # 向左偏移10px
        else:
            self.bg_color = QColor(200, 255, 200)  # 浅绿色(发送气泡)
            self.follow_offset = QPoint(100, -30)    # 向右偏移10px
            
        self.text_color = QColor(70, 70, 70)   # 深灰色
        self.setFont(QFont("Arial", 12, QFont.Bold))
        self.corner_radius = 10
        self.arrow_height = 10
        
        # 字体设置
        self.setFont(QFont("Microsoft YaHei", 12))
        
        # 动画组
        self.animation_group = QSequentialAnimationGroup(self)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制圆角矩形主体
        body_rect = self.rect().adjusted(0, 0, 0, -self.arrow_height)
        painter.setBrush(self.bg_color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(body_rect, self.corner_radius, self.corner_radius)
        
        # 绘制箭头(根据气泡类型决定方向)
        path = QPainterPath()
        arrow_width = 20
        if self.bubble_type == "received":
            # 接收气泡箭头在左侧
            center_x = 30
        else:
            # 发送气泡箭头在右侧
            center_x = self.width() - 30
            
        path.moveTo(center_x - arrow_width//2, body_rect.height())
        path.lineTo(center_x, self.height())
        path.lineTo(center_x + arrow_width//2, body_rect.height())
        painter.drawPath(path)
        
        # 绘制文字(左对齐，带边距)
        painter.setPen(self.text_color)
        text_rect = body_rect.adjusted(10, 5, -10, 0)  # 左右各留10px边距
        painter.drawText(text_rect, Qt.AlignLeft | Qt.TextWordWrap, self.text())

    def calculate_bubble_size(self, text):
        metrics = self.fontMetrics()
        max_width = 300  # 气泡最大宽度
        min_width = 100   # 气泡最小宽度
        
        # 计算文本所需宽度(包括边距)
        text_width = metrics.width(text) + 20  # 左右各10px边距
        
        # 动态确定宽度(不超过最大宽度)
        actual_width = min(max_width, max(min_width, text_width))
        
        # 计算在确定宽度下文本所需高度(考虑换行)
        text_rect = metrics.boundingRect(
            QRect(0, 0, actual_width - 20, 0),  # 减去边距后的实际文本区域宽度
            Qt.TextWordWrap, 
            text
        )
        
        # 基础高度 + 上下边距(各10px) + 箭头高度
        height = text_rect.height() + 20 + self.arrow_height
        
        return QSize(actual_width, height)

    def show_message(self, text):
        """显示气泡消息"""
        self.setText(text)
        size = self.calculate_bubble_size(text)
        self.resize(size)
        
        # 添加到活动气泡列表
        self._active_bubbles.append(self)
        
        # 更新所有气泡位置
        self.update_position()
        
        self.show()
        
    def update_position(self):
        """更新所有活动气泡的位置"""
        if not self.parent():
            return
            
        parent_rect = self.parent().geometry()
        screen_geo = QApplication.primaryScreen().availableGeometry()
        
        # 计算参考位置
        center_x = parent_rect.center().x()
        left_align_x = center_x - 200  # 接收气泡左边界位置
        right_align_x = center_x + 200  # 发送气泡右边界位置
        
        # 从下往上排列气泡
        total_height = 0
        for i, bubble in enumerate(reversed(self._active_bubbles)):
            if not bubble.isVisible():
                continue
                
            # 计算水平位置
            if bubble.bubble_type == "received":
                # 接收气泡：左边界对齐到left_align_x
                new_x = left_align_x
            else:
                # 发送气泡：右边界对齐到right_align_x
                new_x = right_align_x - bubble.width()
                
            # 计算垂直位置
            bubble_y = parent_rect.top() - total_height - bubble.height() - 30
            
            # 边界约束
            new_x = max(screen_geo.left() + 5,
                    min(new_x, 
                        screen_geo.right() - bubble.width() - 5))
            
            # 如果上方空间不足，改为显示在下方
            if bubble_y < screen_geo.top():
                bubble_y = parent_rect.bottom() + total_height + 30
                bubble.arrow_height = -abs(bubble.arrow_height)  # 箭头朝下
            else:
                bubble.arrow_height = abs(bubble.arrow_height)  # 箭头朝上
            
            # 应用位置
            bubble.move(new_x, bubble_y)
            bubble.update()
            
            # 累加高度（包括间距）
            total_height += bubble.height() + self._vertical_spacing

    def fade_out(self):
        """淡出并移除气泡"""
        # 停止所有动画
        self.animation_group.stop()
        
        # 淡出动画
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(500)
        fade_anim.setStartValue(1.0)
        fade_anim.setEndValue(0.0)
        
        # 动画完成后移除
        fade_anim.finished.connect(self._remove_bubble)
        
        self.animation_group.addAnimation(fade_anim)
        self.animation_group.start()

    def _remove_bubble(self):
        """从活动列表中移除气泡"""
        if self in self._active_bubbles:
            self._active_bubbles.remove(self)
        self.hide()
        self.deleteLater()
        
        # 更新剩余气泡的位置
        if self._active_bubbles:
            self._active_bubbles[-1].update_all_bubbles_position()

# 不再使用单例模式
# bubble = SpeechBubble()