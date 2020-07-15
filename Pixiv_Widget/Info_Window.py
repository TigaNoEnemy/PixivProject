#!/usr/bin/env python3
from qtcreatorFile import info_window_1
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, pyqtSignal


import cgitb
cgitb.enable(format='text', logdir='log_file')
class _info_window(QMainWindow, info_window_1.Ui_MainWindow):
    """docstring for _info_window"""
    closed = pyqtSignal()
    def __init__(self, parent):
        super(_info_window, self).__init__()
        self.parent = parent
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.command_to_action()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.move_self_to_center()
        self.move_children_to_certer()

    def move_children_to_certer(self):
        from PyQt5.QtWidgets import QWidget

        width = self.width()
        children = self.children()
        for i in children:
            if isinstance(i, QWidget):
                child_w = i.width()
                child_y = i.y()
                child_new_x = (width-child_w)//2
                i.move(child_new_x, child_y)

    def move_self_to_center(self):
        parent_x = self.parent.x()
        parent_y = self.parent.y()
        parent_w = self.parent.width()
        parent_h = self.parent.height()
        width = self.width()
        height = self.height()

        x = (parent_w - width)//2
        y = (parent_h - height)//2
        self.move(x+parent_x, y+parent_y)

    def command_to_action(self):
        self.pushButton.clicked.connect(self.close)

    def closeEvent(self, qevent):
        self.closed.emit()
        del self

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    a = _info_window()
    a.show()
    sys.exit(app.exec_())