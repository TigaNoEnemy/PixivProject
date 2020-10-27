# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'small_pic_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from Pixiv_Widget.Clickable_Label import clickable_label


class Ui_small_pic_frame(object):
    def setupUi(self, small_pic_frame):
        small_pic_frame.setObjectName("small_pic_frame")
        small_pic_frame.resize(240, 411)
        self.frame = QtWidgets.QFrame(small_pic_frame)
        self.frame.setGeometry(QtCore.QRect(0, 0, 240, 411))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textLabel = QtWidgets.QLabel(self.frame)
        self.textLabel.setGeometry(QtCore.QRect(5, 234, 234, 51))
        self.textLabel.setStyleSheet("")
        self.textLabel.setWordWrap(True)
        self.textLabel.setObjectName("textLabel")
        self.s_saveButton = QtWidgets.QPushButton(self.frame)
        self.s_saveButton.setGeometry(QtCore.QRect(0, 370, 121, 41))
        self.s_saveButton.setObjectName("s_saveButton")
        self.likeButton = QtWidgets.QPushButton(self.frame)
        self.likeButton.setGeometry(QtCore.QRect(120, 370, 121, 41))
        self.likeButton.setObjectName("likeButton")
        self.authLabel = QtWidgets.QLabel(self.frame)
        self.authLabel.setGeometry(QtCore.QRect(5, 285, 234, 41))
        self.authLabel.setObjectName("authLabel")
        self.picnNumLabel = QtWidgets.QLabel(self.frame)
        self.picnNumLabel.setGeometry(QtCore.QRect(204, 0, 30, 30))
        self.picnNumLabel.setStyleSheet("background-color: rgba(122, 122, 122, 150);\n"
"font: 16pt \"Noto Sans CJK SC\";")
        self.picnNumLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.picnNumLabel.setObjectName("picnNumLabel")
        self.picLabel = clickable_label(self.frame)
        self.picLabel.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.picLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.picLabel.setObjectName("picLabel")

        self.retranslateUi(small_pic_frame)
        QtCore.QMetaObject.connectSlotsByName(small_pic_frame)

    def retranslateUi(self, small_pic_frame):
        _translate = QtCore.QCoreApplication.translate
        small_pic_frame.setWindowTitle(_translate("small_pic_frame", "Form"))
        self.textLabel.setText(_translate("small_pic_frame", "TextLabel"))
        self.s_saveButton.setText(_translate("small_pic_frame", "PushButton"))
        self.likeButton.setText(_translate("small_pic_frame", "PushButton"))
        self.authLabel.setText(_translate("small_pic_frame", "TextLabel"))
        self.picnNumLabel.setText(_translate("small_pic_frame", "TextLabel"))
        self.picLabel.setText(_translate("small_pic_frame", "TextLabel"))
