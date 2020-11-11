#!/usr/bin/env python3
import sys
sys.path.append('.')
from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QPropertyAnimation


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
        self.setStyleSheet("QToolTip{background-color: #000000; color: #FFFFFF; border: none}")
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
        temp_path = self.info['temp_path']
        illust_id = self.info['illust_id']
        file = f"{temp_path}/{illust_id}"
        pic = QPixmap(file)
        try:
            pic = pic.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        except AttributeError:
            pass
        else:
            self.setPixmap(pic)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    m = QMainWindow()
    m.resize(150, 150)
    info = {'temp_path': '/home/minming/Desktop/人像', 'illust_id': '7.png'}
    
    a = Largable_Label(m, info=info)
    a.resize(100, 100)
    a.move((m.width()-a.width())/2, (m.height()-a.height())/2)
    a.set_original_geometry(a.x(), a.y(), a.width(), a.height())
    #pic = pic.scaled(a.width(), a.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    m.move(2000, 1000)
    m.show()
    sys.exit(app.exec_())