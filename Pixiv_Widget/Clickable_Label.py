#!/usr/bin/env python3

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal, QTimer

import cgitb
cgitb.enable(format='text', logdir='log_file')

class clickable_label(QLabel):
    click = pyqtSignal(dict)
    double_click = pyqtSignal(dict)
    right_click = pyqtSignal(dict)
    # force_reload_signal = pyqtSignal(dict)
    # download_pic_signal = pyqtSignal(dict)
    def __init__(self, parent, info={}, double_click_time=200):
        super(clickable_label, self).__init__(parent)
        self.info = info
        self.double_click_time = double_click_time
        self.clicked_timer = QTimer()
        self.clicked_timer.timeout.connect(self.emit_click)

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1:
            if self.clicked_timer.isActive():
                self.clicked_timer.stop()
                self.double_click.emit(self.info)
            else:
                self.clicked_timer.start(self.double_click_time)
            qevent.accept()

        elif qevent.button() == 2:
            self.right_click.emit(self.info)
            print(0)
            qevent.accept()

    def emit_click(self):
        self.clicked_timer.stop()
        self.click.emit(self.info)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)

    a = clickable_label(None)

    a.click.connect(lambda x: [print(x), a.click.disconnect()])
    a.double_click.connect(lambda x: print(x))

    a.move(2100, 1100)
    a.resize(100, 50)

    a.show()

    sys.exit(app.exec_())