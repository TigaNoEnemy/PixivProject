# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'infoFrame.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_infoFrame(object):
    def setupUi(self, infoFrame):
        infoFrame.setObjectName("infoFrame")
        infoFrame.resize(1041, 82)
        self.user_pic_label = Show_Head_Label(infoFrame)
        self.user_pic_label.setGeometry(QtCore.QRect(7, 11, 61, 61))
        self.user_pic_label.setText("")
        self.user_pic_label.setObjectName("user_pic_label")
        self.authText = Username_Label(infoFrame)
        self.authText.setGeometry(QtCore.QRect(80, 49, 171, 31))
        self.authText.setText("")
        self.authText.setWordWrap(True)
        self.authText.setObjectName("authText")
        self.moreButton = QtWidgets.QPushButton(infoFrame)
        self.moreButton.setGeometry(QtCore.QRect(950, 40, 80, 31))
        self.moreButton.setObjectName("moreButton")
        self.saveButton = QtWidgets.QPushButton(infoFrame)
        self.saveButton.setGeometry(QtCore.QRect(860, 40, 80, 31))
        self.saveButton.setObjectName("saveButton")
        self.escapeDownloadPageButton = QtWidgets.QPushButton(infoFrame)
        self.escapeDownloadPageButton.setGeometry(QtCore.QRect(950, 40, 80, 31))
        self.escapeDownloadPageButton.setObjectName("escapeDownloadPageButton")
        self.titleText = Auto_Text_Label(infoFrame)
        self.titleText.setGeometry(QtCore.QRect(80, 11, 170, 31))
        self.titleText.setText("")
        self.titleText.setWordWrap(False)
        self.titleText.setObjectName("titleText")
        self.text_scroll = text_scroll(infoFrame)
        self.text_scroll.setGeometry(QtCore.QRect(260, 0, 521, 81))
        self.text_scroll.setObjectName("text_scroll")

        self.retranslateUi(infoFrame)
        QtCore.QMetaObject.connectSlotsByName(infoFrame)

    def retranslateUi(self, infoFrame):
        _translate = QtCore.QCoreApplication.translate
        infoFrame.setWindowTitle(_translate("infoFrame", "Frame"))
        self.moreButton.setText(_translate("infoFrame", "更多"))
        self.saveButton.setText(_translate("infoFrame", "保存原图"))
        self.escapeDownloadPageButton.setText(_translate("infoFrame", "返回"))
from Pixiv_Widget.My_Label import Auto_Text_Label, Username_Label
from Pixiv_Widget.My_Widget import Show_Head_Label
from Pixiv_Widget.Text_Scroll import text_scroll
