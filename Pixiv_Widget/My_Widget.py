#!/usr/bin/env python3
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

import cgitb
cgitb.enable(format='text', logdir='log_file')
class my_widget(QWidget):
    def __init__(self, parent=None, flag=''):
        super(my_widget, self).__init__(parent)
        self.flag = flag
        self.is_loading = True
        self.rotate = 90
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_rotate)
        self.timer.start(5)

    def change_rotate(self):
        self.rotate += 1

    def set_loading(self, p):
        self.is_loading = p

    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF, Qt

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = (width-50)//2
            load_y = (height-50)//2

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, 50, 50)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x, load_y, 50, 50), -self.rotate*16, -90*16)# 画圆环, 进度条
        else:
            self.timer.stop()

        self.update()

class Scroll_Widget(QWidget):
    """docstring for Scroll_Widget"""
    def adjust_size(self):
        height = 0
        for i in self.children():
            i.move(i.x(), height)
            height += i.height()
            height += 5
        self.resize(self.width(), height)
        

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    a = my_widget()
    a.set_loading(True)
    a.show()
    sys.exit(app.exec_())