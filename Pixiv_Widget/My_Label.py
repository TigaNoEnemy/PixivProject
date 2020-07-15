#!/usr/bin/env python3

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, Qt


import cgitb
cgitb.enable(format='text', logdir='log_file')
class my_label(QLabel):
    """自定义我的label控件，用于标签点击和画师点击"""
    clicked = pyqtSignal(dict)
    def __init__(self, parent, info={}):
        super(my_label, self).__init__(parent)
        self.info = info # tag、text，text用于显示，tag用于app逻辑处理
        self.check_info()

    def check_info(self):
        key = ['text', 'tag']
        need_key = []
        need_not_key = []
        for i in self.info:
            if i not in key:
                need_not_key.append(i)
        for i in key:
            if i not in self.info:
                need_key.append(i)
        if need_key or need_not_key:
            raise KeyError(f"my_label doesn't need {need_not_key} and lack {need_key}")

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