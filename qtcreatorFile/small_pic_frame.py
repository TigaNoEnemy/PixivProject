# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtcreatorFile/small_pic_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_small_pic_frame(object):
    def setupUi(self, small_pic_frame):
        small_pic_frame.setObjectName("small_pic_frame")
        small_pic_frame.resize(240, 411)
        small_pic_frame.setStyleSheet("")
        self.frame = QtWidgets.QFrame(small_pic_frame)
        self.frame.setGeometry(QtCore.QRect(0, 0, 240, 411))
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textLabel = QtWidgets.QLabel(self.frame)
        self.textLabel.setGeometry(QtCore.QRect(5, 234, 235, 51))
        self.textLabel.setStyleSheet("")
        self.textLabel.setText("")
        self.textLabel.setWordWrap(True)
        self.textLabel.setObjectName("textLabel")
        self.s_saveButton = QtWidgets.QPushButton(self.frame)
        self.s_saveButton.setGeometry(QtCore.QRect(0, 370, 120, 41))
        self.s_saveButton.setStyleSheet("")
        self.s_saveButton.setObjectName("s_saveButton")
        self.authLabel = QtWidgets.QLabel(self.frame)
        self.authLabel.setGeometry(QtCore.QRect(5, 285, 235, 41))
        self.authLabel.setStyleSheet("")
        self.authLabel.setText("")
        self.authLabel.setObjectName("authLabel")
        self.picnNumLabel = QtWidgets.QLabel(self.frame)
        self.picnNumLabel.setGeometry(QtCore.QRect(204, 0, 30, 30))
        self.picnNumLabel.setStyleSheet("")
        self.picnNumLabel.setText("")
        self.picnNumLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.picnNumLabel.setObjectName("picnNumLabel")
        self.likeButton = QtWidgets.QPushButton(self.frame)
        self.likeButton.setGeometry(QtCore.QRect(120, 370, 120, 41))
        self.likeButton.setStyleSheet("")
        self.likeButton.setObjectName("likeButton")
        self.picLabel = clickable_label(self.frame)
        self.picLabel.setGeometry(QtCore.QRect(0, 0, 240, 234))
        self.picLabel.setStyleSheet("")
        self.picLabel.setText("")
        self.picLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.picLabel.setObjectName("picLabel")
        self.textLabel.raise_()
        self.s_saveButton.raise_()
        self.authLabel.raise_()
        self.likeButton.raise_()
        self.picLabel.raise_()
        self.picnNumLabel.raise_()

        self.retranslateUi(small_pic_frame)
        QtCore.QMetaObject.connectSlotsByName(small_pic_frame)

    def retranslateUi(self, small_pic_frame):
        _translate = QtCore.QCoreApplication.translate
        small_pic_frame.setWindowTitle(_translate("small_pic_frame", "Form"))
        self.s_saveButton.setText(_translate("small_pic_frame", "PushButton"))
        self.likeButton.setText(_translate("small_pic_frame", "PushButton"))
from Pixiv_Widget.Clickable_Label import clickable_label
