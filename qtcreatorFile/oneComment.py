# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtcreatorFile\oneComment.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_oneComment(object):
    def setupUi(self, oneComment):
        oneComment.setObjectName("oneComment")
        oneComment.resize(340, 200)
        self.frame = QtWidgets.QFrame(oneComment)
        self.frame.setGeometry(QtCore.QRect(0, 0, 340, 200))
        self.frame.setStyleSheet("background-color: rgb(48, 51, 41);\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.user_pic_label = QtWidgets.QLabel(self.frame)
        self.user_pic_label.setGeometry(QtCore.QRect(10, 10, 50, 50))
        self.user_pic_label.setStyleSheet("color: rgb(255, 255, 255);")
        self.user_pic_label.setText("")
        self.user_pic_label.setObjectName("user_pic_label")
        self.user_name_label = QtWidgets.QLabel(self.frame)
        self.user_name_label.setGeometry(QtCore.QRect(70, 10, 121, 20))
        self.user_name_label.setStyleSheet("\n"
"color: rgb(255, 255, 255);")
        self.user_name_label.setText("")
        self.user_name_label.setObjectName("user_name_label")
        self.comment_text = QtWidgets.QTextBrowser(self.frame)
        self.comment_text.setGeometry(QtCore.QRect(0, 70, 338, 100))
        self.comment_text.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 51, 41);\n"
"border: none;")
        self.comment_text.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.comment_text.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.comment_text.setObjectName("comment_text")
        self.time_label = QtWidgets.QLabel(self.frame)
        self.time_label.setGeometry(QtCore.QRect(70, 40, 211, 20))
        self.time_label.setStyleSheet("color: rgb(209, 209, 209);\n"
"color: rgb(147, 147, 147);")
        self.time_label.setText("")
        self.time_label.setObjectName("time_label")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 190, 343, 18))
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")

        self.retranslateUi(oneComment)
        QtCore.QMetaObject.connectSlotsByName(oneComment)

    def retranslateUi(self, oneComment):
        _translate = QtCore.QCoreApplication.translate
        oneComment.setWindowTitle(_translate("oneComment", "Form"))
        self.label.setText(_translate("oneComment", "<hr>"))
