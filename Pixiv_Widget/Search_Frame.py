#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from qtcreatorFile import search_frame
from PyQt5.QtWidgets import QFrame


class search_frame(QFrame, search_frame.Ui_Frame):
    def __init__(self, parent=None, main=None, info={}):
        super(search_frame, self).__init__(parent)
        self.setupUi(self)
        self.action_to_command()
        self.set_font_style()
        self.init_search_frame()
        self.main = main
        self.info = info
        self.searchFrameIsShow = False

    def action_to_command(self):
        self.cancelSearchButton.clicked.connect(self.hide_search_frame)
        self.searchButton.clicked.connect(lambda: self.main._search(isMoreButton=False))

    def set_font_style(self):
        F = """QPushButton{color: rgb(255, 255, 255);}
                                          QPushButton:hover{background-color:lightblue; color:black}
                                          QPushButton{border:2px}
                                          QPushButton{border-radius:15px}
                                          QPushButton{padding:2px 4px}
                                          QPushButton:pressed{background-color:black}
                                          """
        self.searchButton.setStyleSheet(F)
        self.cancelSearchButton.setStyleSheet(F)

    def init_search_frame(self):
        target = ['标签', '画师', '作品id', '画师id']
        for i in target:
            self.searchComboBox.addItem(i)
        self.searchComboBox.setCurrentText('标签')

    def show_search_frame(self):
        from PyQt5 import sip
        from PyQt5.QtCore import QPropertyAnimation
        from PyQt5.QtCore import QRect

        if self.searchFrameIsShow:
            return

        def change_search_frame_status():
            self.searchFrameIsShow = True
            self.main.searchButton.disconnect()
            self.main.searchButton.clicked.connect(self.hide_search_frame)
            self.search_frame_animation.deleteLater()
            sip.delete(self.search_frame_animation)
            del self.search_frame_animation
            self.searchLineEdit.setFocus()

        searchFrame_w = self.width()
        self.search_frame_animation = QPropertyAnimation(self)
        self.search_frame_animation.setPropertyName(b'geometry')
        self.search_frame_animation.setTargetObject(self)
        self.search_frame_animation.setStartValue(QRect(0, -120, searchFrame_w, 0))
        self.search_frame_animation.setEndValue(QRect(0, 0, searchFrame_w, 120))
        self.search_frame_animation.setDuration(100)
        self.search_frame_animation.finished.connect(change_search_frame_status)
        self.search_frame_animation.start()

    def hide_search_frame(self):
        from PyQt5 import sip
        from PyQt5.QtCore import QPropertyAnimation, QRect

        if not self.searchFrameIsShow:
            return

        def change_search_frame_status():
            self.searchFrameIsShow = False
            self.main.searchButton.disconnect()
            self.main.searchButton.clicked.connect(self.show_search_frame)
            self.search_frame_animation.deleteLater()
            sip.delete(self.search_frame_animation)
            del self.search_frame_animation

        searchFrame_w = self.width()
        self.search_frame_animation = QPropertyAnimation(self)
        self.search_frame_animation.setPropertyName(b'geometry')
        self.search_frame_animation.setTargetObject(self)
        self.search_frame_animation.setStartValue(QRect(0, 0, searchFrame_w, 120))
        self.search_frame_animation.setEndValue(QRect(0, -120, searchFrame_w, 0))
        self.search_frame_animation.setDuration(100)
        self.search_frame_animation.finished.connect(change_search_frame_status)
        self.search_frame_animation.start()

    # def keyPressEvent(self, qevent):
    #     if qevent.key() == 16777216: # Esc
    #         self.hide_search_frame()
    #     elif qevent.key() == 16777220:    # Enter
    #         self.show_search_frame()

    def resizeEvent(self, qevent):
        width = self.width()

        searchLineEdit_x = self.searchLineEdit.x()
        searchLineEdit_h = self.searchLineEdit.height()
        self.searchLineEdit.resize(width - searchLineEdit_x - 231, searchLineEdit_h)
        searchComboBox_y = self.searchComboBox.y()
        self.searchComboBox.move(width - 231, searchComboBox_y)
        self.searchButton.move(width - 151, searchComboBox_y)
        self.cancelSearchButton.move(width - 81, searchComboBox_y)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from PyQt5.QtCore import QRect
    import sys

    app = QApplication(sys.argv)
    p = QMainWindow()
    s_f = search_frame(p)
    s_f.setGeometry(QRect(0,-120,1041,120))
    s_f.setFocus()
    p.resize(1041,120)
    p.show()
    sys.exit(app.exec_())