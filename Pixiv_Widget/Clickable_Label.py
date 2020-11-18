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
        self.clicked_timer = QTimer()
        self.clicked_timer.timeout.connect(self.emit_click)
        #self.setStyleSheet("QToolTip{background-color: #000000; color: #FFFFFF; border: none}")

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1:
            if self.clicked_timer.isActive():
                self.clicked_timer.stop()
                self.double_click.emit(self.info)
            else:
                self.clicked_timer.start(self.double_click_time)

    def emit_click(self):
        self.clicked_timer.stop()
        self.click.emit(self.info)