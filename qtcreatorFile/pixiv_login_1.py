# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1158, 829)
        MainWindow.setStyleSheet("")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.widget = QtWidgets.QWidget(self.centralWidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 520, 431))
        self.widget.setStyleSheet("background-color: rgb(102, 206, 255);")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(70, 120, 71, 41))
        self.label.setStyleSheet("font: 20pt \"Noto Sans CJK SC\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(210, 20, 141, 61))
        self.label_2.setStyleSheet("font: 20pt \"Noto Sans CJK SC\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(70, 230, 71, 41))
        self.label_3.setStyleSheet("font: 20pt \"Noto Sans CJK SC\";")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(220, 340, 111, 51))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 130, 281, 26))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(150, 240, 281, 26))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.autoLogin = QtWidgets.QCheckBox(self.widget)
        self.autoLogin.setGeometry(QtCore.QRect(420, 400, 82, 24))
        self.autoLogin.setStyleSheet("background-color: rgb(102, 206, 255);")
        self.autoLogin.setObjectName("autoLogin")
        self.exit_button = QtWidgets.QPushButton(self.widget)
        self.exit_button.setGeometry(QtCore.QRect(490, 0, 30, 30))
        self.exit_button.setText("")
        self.exit_button.setObjectName("exit_button")
        self.autoLogin_2 = QtWidgets.QWidget(self.centralWidget)
        self.autoLogin_2.setGeometry(QtCore.QRect(0, 0, 520, 431))
        self.autoLogin_2.setObjectName("autoLogin_2")
        self.loginGIF = QtWidgets.QLabel(self.autoLogin_2)
        self.loginGIF.setGeometry(QtCore.QRect(0, 0, 520, 321))
        self.loginGIF.setStyleSheet("background-color: rgb(102, 206, 255);")
        self.loginGIF.setAlignment(QtCore.Qt.AlignCenter)
        self.loginGIF.setObjectName("loginGIF")
        self.loginText = QtWidgets.QLabel(self.autoLogin_2)
        self.loginText.setGeometry(QtCore.QRect(0, 321, 520, 110))
        self.loginText.setStyleSheet("font: 20pt \"Noto Sans CJK SC\";\n"
"background-color: rgb(102, 206, 255);")
        self.loginText.setAlignment(QtCore.Qt.AlignCenter)
        self.loginText.setObjectName("loginText")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "账号："))
        self.label_2.setText(_translate("MainWindow", "Pixiv登录"))
        self.label_3.setText(_translate("MainWindow", "密码："))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.autoLogin.setText(_translate("MainWindow", "自动登录"))
        self.loginGIF.setText(_translate("MainWindow", "TextLabel"))
        self.loginText.setText(_translate("MainWindow", "登录中......"))
