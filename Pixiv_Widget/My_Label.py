#!/usr/bin/env python3
import sys
sys.path.append('.')
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor, QFont, QFontMetrics
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QPropertyAnimation, QTimer


import cgitb
cgitb.enable(format='text', logdir='log_file')
class my_label(QLabel):
    """自定义我的label控件，用于标签点击和画师点击"""
    clicked = pyqtSignal(dict)
    def __init__(self, parent, info={}):
        super(my_label, self).__init__(parent)
        self.info = info # tag、text，text用于显示，tag用于app逻辑处理
    #     self.check_info()

    # def check_info(self):
    #     key = ['text', 'tag']
    #     need_key = []
    #     need_not_key = []
    #     for i in self.info:
    #         if i not in key:
    #             need_not_key.append(i)
    #     for i in key:
    #         if i not in self.info:
    #             need_key.append(i)
    #     if need_key or need_not_key:
    #         raise KeyError(f"Largable_Label doesn't need {need_not_key} and lack {need_key}")

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1:
            self.clicked.emit(self.info)

    def enterEvent(self, qevent):
        text = self.info.get('text', self.text())
        self.info['text'] = text
        self.setCursor(Qt.PointingHandCursor)
        self.setText(f'<u>{self.info["text"]}</u>')

    def leaveEvent(self, qevent):
        self.setText(self.info['text'])

class Largable_Label(QLabel):
    """用于显示图片，当鼠标悬停于上时，放大图片，当鼠标移走时恢复原样"""
    times = 1.2 # 放大倍数
    def __init__(self, parent=None, info={}):
        super(Largable_Label, self).__init__(parent)
        self.animation_is_start = False
        self.info = info
        #self.setStyleSheet("QToolTip{background-color: #000000; color: #FFFFFF; border: none}")
        self.setToolTip(info['illust']['title'])

    def add_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0) # 偏移
        self.shadow.setBlurRadius(20)   # 阴影半径
        self.shadow.setColor(QColor("#000000"))
        self.setGraphicsEffect(self.shadow)

    def drop_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0) # 偏移
        self.shadow.setBlurRadius(0)   # 阴影半径
        self.shadow.setColor(QColor("#000000"))
        self.setGraphicsEffect(self.shadow)
    
    def set_original_geometry(self, x, y, width, height):
        self.o_width = width
        self.o_height = height
        self.o_x = x
        self.o_y = y

    def enterEvent(self, qevent):
        super(Largable_Label, self).enterEvent(qevent)
        if not hasattr(self, 'o_x'):
            return None
        self.raise_()
        if hasattr(self, 'animation'):
            self.animation.stop()
        old_rect = self.geometry()

        n_width = self.o_width * self.times
        n_height = self.o_height * self.times
        
        new_rect = QRect(
            self.o_x - (n_width - self.o_width) / 2, 
            self.o_y - (n_height - self.o_height) / 2, 
            n_width,
            n_height
            )
        if not self.animation_is_start:
            self.add_shadow()
            self.resizeAnimation(old_rect, new_rect, 'larging_complete')

    def resizeAnimation(self, old_rect, new_rect, state):
        if hasattr(self, 'is_loading'):
            if self.is_loading:
                return 
        try:
            self.animation.disconnect()
        except:
            pass
        self.animation = QPropertyAnimation(self)
        self.animation.setPropertyName(b'geometry')
        self.animation.setTargetObject(self)
        self.animation.setStartValue(old_rect)
        self.animation.setEndValue(new_rect)
        self.animation.setDuration(100)
        self.animation.start()

    def leaveEvent(self, qevent):
        super(Largable_Label, self).leaveEvent(qevent)
        if not hasattr(self, 'o_x'):
            return None
        if hasattr(self, 'animation'):
            self.animation.stop()
        old_rect = self.geometry()
        new_rect = QRect(
            self.o_x, 
            self.o_y,
            self.o_width,
            self.o_height
            )
        if not self.animation_is_start:
            self.drop_shadow()
            self.resizeAnimation(old_rect, new_rect, 'shorting_complete')

    def resizeEvent(self, qevent):
        super(Largable_Label, self).resizeEvent(qevent)
        width = self.width()
        height = self.height()
        illust_id = self.info['illust_id']
        file = self.file
        pic = QPixmap(file)
        if not pic.isNull():
            pic = pic.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(pic)

class Loading_Label(QLabel):
    """加载图片是转圈, 暂时无用"""
    def __init__(self, parent, *args, **kwargs):
        super(Loading_Label, self).__init__(parent, *args, **kwargs)
        self.is_loading = True
        self.rotate = 90
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.change_rotate)
        self.loading_timer.start(5)

    def change_rotate(self):
        self.rotate += 1
        
    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF, Qt
        super(Loading_Label, self).paintEvent(qevent)

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = width/2//2
            load_y = height/2//2

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, width-width/2, height-height/2)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x, load_y, width-width/2, height-height/2), -self.rotate*16, -90*16)# 画圆环, 进度条
        else:
            if self.loading_timer.isActive():
                self.loading_timer.stop()

        self.update()

class Auto_Text_Label(QLabel):
    """
    用于显示文字的label，在使用setText方法时会自动调整字体大小以求尽量显示完全
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setText(self, s):
        super().setText(s)
        init_font_size = 20
        self.setFont(QFont("Microsoft YaHei", init_font_size))
        font = self.font()
        fm = QFontMetrics(font)
        rec = fm.boundingRect(self.text())

        while (rec.width() > self.width() or rec.height() > self.height()) and init_font_size > 1:
            init_font_size -= 1
            self.setFont(QFont("Microsoft YaHei", init_font_size))
            font = self.font()
            fm = QFontMetrics(font)
            rec = fm.boundingRect(self.text())

class Username_Label(my_label, Auto_Text_Label):
    """
    用于显示用户名，可点击，自动调整字体大小
    """
    pass
        

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    m = QMainWindow()
    m.resize(150, 150)
    info = {'temp_path': '/home/minming/Desktop/人像', 'illust_id': '7.png'}
    
    a = Loading_Label(m)
    a.resize(100, 100)
    a.move((m.width()-a.width())/2, (m.height()-a.height())/2)
    #a.set_original_geometry(a.x(), a.y(), a.width(), a.height())
    #pic = pic.scaled(a.width(), a.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    m.move(2000, 1000)
    m.show()
    sys.exit(app.exec_())