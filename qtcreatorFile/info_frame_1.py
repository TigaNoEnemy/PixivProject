# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtcreatorFile\infoFrame.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1041, 82)
        Frame.setStyleSheet("background-color: rgb(29, 23, 31);")
        self.user_pic_label = Show_Head_Label(Frame)
        self.user_pic_label.setGeometry(QtCore.QRect(7, 11, 61, 61))
        self.user_pic_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.user_pic_label.setText("")
        self.user_pic_label.setObjectName("user_pic_label")
        self.authText = my_label(Frame)
        self.authText.setGeometry(QtCore.QRect(80, 49, 141, 21))
        self.authText.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.authText.setText("")
        self.authText.setWordWrap(True)
        self.authText.setObjectName("authText")
        self.moreButton = QtWidgets.QPushButton(Frame)
        self.moreButton.setGeometry(QtCore.QRect(950, 40, 80, 31))
        self.moreButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.moreButton.setObjectName("moreButton")
        self.saveButton = QtWidgets.QPushButton(Frame)
        self.saveButton.setGeometry(QtCore.QRect(860, 40, 80, 31))
        self.saveButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.saveButton.setObjectName("saveButton")
        self.escapeDownloadPageButton = QtWidgets.QPushButton(Frame)
        self.escapeDownloadPageButton.setGeometry(QtCore.QRect(950, 40, 80, 31))
        self.escapeDownloadPageButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.escapeDownloadPageButton.setObjectName("escapeDownloadPageButton")
        self.titleText = QtWidgets.QLabel(Frame)
        self.titleText.setGeometry(QtCore.QRect(80, 11, 170, 31))
        self.titleText.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);")
        self.titleText.setText("")
        self.titleText.setWordWrap(True)
        self.titleText.setObjectName("titleText")
        self.text_scroll = text_scroll(Frame)
        self.text_scroll.setGeometry(QtCore.QRect(260, 0, 521, 81))
        self.text_scroll.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"color: rgb(255, 255, 255);\n"
"border: none")
        self.text_scroll.setObjectName("text_scroll")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.moreButton.setText(_translate("Frame", "更多"))
        self.saveButton.setText(_translate("Frame", "保存原图"))
        self.escapeDownloadPageButton.setText(_translate("Frame", "返回"))
from Pixiv_Widget.My_Label import my_label
from Pixiv_Widget.My_Widget import Show_Head_Label
from Pixiv_Widget.Text_Scroll import text_scroll
