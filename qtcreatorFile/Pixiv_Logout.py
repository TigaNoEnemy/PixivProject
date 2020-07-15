# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logout.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(463, 276)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(114, 50, 311, 91))
        self.label.setStyleSheet("font: 20pt \"Noto Sans CJK SC\";")
        self.label.setObjectName("label")
        self.OKButton = QtWidgets.QPushButton(self.centralWidget)
        self.OKButton.setGeometry(QtCore.QRect(120, 190, 80, 26))
        self.OKButton.setObjectName("OKButton")
        self.cancelButton = QtWidgets.QPushButton(self.centralWidget)
        self.cancelButton.setGeometry(QtCore.QRect(250, 190, 80, 26))
        self.cancelButton.setObjectName("cancelButton")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "确定注销吗(⊙o⊙)?"))
        self.OKButton.setText(_translate("MainWindow", "确定"))
        self.cancelButton.setText(_translate("MainWindow", "取消"))
