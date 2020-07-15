#!/usr/bin/env python3

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QTimer

import cgitb
cgitb.enable(format='text', logdir='log_file')

class clickable_label(QLabel):
    click = pyqtSignal(dict)
    double_click = pyqtSignal(dict)
    def __init__(self, parent, info={}, double_click_time=200):
        super(clickable_label, self).__init__(parent)
        self.info = info
        self.double_click_time = double_click_time
        self.timer = QTimer()
        self.timer.timeout.connect(self.emit_click)

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1:
            if self.timer.isActive():
                self.timer.stop()
                self.double_click.emit(self.info)
            else:
                self.timer.start(self.double_click_time)

    def emit_click(self):
        self.timer.stop()
        self.click.emit(self.info)