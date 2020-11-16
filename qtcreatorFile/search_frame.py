# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'search_frame.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1041, 120)
        #Frame.setStyleSheet("background-color: rgb(25, 25, 25);")
        self.searchLineEdit = QtWidgets.QLineEdit(Frame)
        self.searchLineEdit.setGeometry(QtCore.QRect(20, 60, 790, 26))
        #self.searchLineEdit.setStyleSheet("color: rgb(255, 255, 255);\n"
# "background-color: rgb(50, 50, 50);")
        self.searchLineEdit.setObjectName("searchLineEdit")
        self.cancelSearchButton = QtWidgets.QPushButton(Frame)
        self.cancelSearchButton.setGeometry(QtCore.QRect(960, 60, 61, 26))
        self.cancelSearchButton.setObjectName("cancelSearchButton")
        self.searchComboBox = QtWidgets.QComboBox(Frame)
        self.searchComboBox.setGeometry(QtCore.QRect(810, 60, 72, 26))
        #self.searchComboBox.setStyleSheet("color: rgb(255, 255, 255);\n"
# "background-color: rgb(50, 50, 50);")
        self.searchComboBox.setObjectName("searchComboBox")
        self.searchButton = QtWidgets.QPushButton(Frame)
        self.searchButton.setGeometry(QtCore.QRect(890, 60, 61, 26))
        self.searchButton.setObjectName("searchButton")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.cancelSearchButton.setText(_translate("Frame", "取消"))
        self.searchButton.setText(_translate("Frame", "搜索"))
