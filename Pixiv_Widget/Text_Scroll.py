#!/usr/bin/env python3
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal, QTimer


import cgitb
cgitb.enable(format='text', logdir='log_file')
def main():
    from PyQt5.QtWidgets import QApplication
    import sys
    _text = f'{"p" * 1000}'
    app = QApplication(sys.argv)
    a = text_scroll(parent=None)
    a.setText(_text)
    a.click.connect(lambda: print('发射！！'))
    a.setStyleSheet('color: rgb(0, 0, 0);border-width:0;border-style:outset')
    a.show()
    sys.exit(app.exec_())


class text_scroll(QTextEdit):
    click = pyqtSignal(QMouseEvent)
    def __init__(self, parent):
        super(text_scroll, self).__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet('color: rgb(255, 255, 255);border-width:0;border-style:outset;')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.dont_send = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.dont_send_click_signal)

    def dont_send_click_signal(self):
        self.dont_send = True
        self.timer.stop()

    def mouseReleaseEvent(self, qevent):
        self.timer.stop()
        if not self.dont_send:
            self.click.emit(qevent)
        self.dont_send = False

    def mousePressEvent(self, qevent):
        super(text_scroll, self).mousePressEvent(qevent)
        self.timer.start(150)


if __name__ == '__main__':
    main()