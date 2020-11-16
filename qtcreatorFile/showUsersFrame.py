# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userinfo.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1257, 811)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.showUserFrame = QtWidgets.QFrame(self.centralWidget)
        self.showUserFrame.setGeometry(QtCore.QRect(50, 160, 791, 371))
        #self.showUserFrame.setStyleSheet("background-color: rgb(76, 184, 255);")
        self.showUserFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.showUserFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.showUserFrame.setObjectName("showUserFrame")
        self.userHeadLabel = QtWidgets.QLabel(self.showUserFrame)
        self.userHeadLabel.setGeometry(QtCore.QRect(30, 20, 50, 50))
        #self.userHeadLabel.setStyleSheet("background-color: rgb(255, 228, 249);")
        self.userHeadLabel.setObjectName("userHeadLabel")
        self.usernameLabel = QtWidgets.QLabel(self.showUserFrame)
        self.usernameLabel.setGeometry(QtCore.QRect(90, 50, 171, 20))
        #self.usernameLabel.setStyleSheet("background-color: rgb(175, 255, 246);")
        self.usernameLabel.setObjectName("usernameLabel")
        self.label = QtWidgets.QLabel(self.showUserFrame)
        self.label.setGeometry(QtCore.QRect(30, 110, 234, 234))
        #self.label.setStyleSheet("background-color: rgb(232, 255, 148);")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.showUserFrame)
        self.label_2.setGeometry(QtCore.QRect(530, 110, 234, 234))
        #self.label_2.setStyleSheet("background-color: rgb(232, 255, 148);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.showUserFrame)
        self.label_3.setGeometry(QtCore.QRect(280, 110, 234, 234))
        #self.label_3.setStyleSheet("background-color: rgb(232, 255, 148);")
        self.label_3.setObjectName("label_3")
        self.followButton = QtWidgets.QPushButton(self.showUserFrame)
        self.followButton.setGeometry(QtCore.QRect(350, 40, 51, 30))
        self.followButton.setObjectName("followButton")
        self.collectionButton = QtWidgets.QPushButton(self.showUserFrame)
        self.collectionButton.setGeometry(QtCore.QRect(410, 40, 51, 30))
        self.collectionButton.setObjectName("collectionButton")
        self.illustButton = QtWidgets.QPushButton(self.showUserFrame)
        self.illustButton.setGeometry(QtCore.QRect(470, 40, 51, 30))
        self.illustButton.setObjectName("illustButton")
        self.itsFollowButton = QtWidgets.QPushButton(self.showUserFrame)
        self.itsFollowButton.setGeometry(QtCore.QRect(530, 40, 51, 30))
        self.itsFollowButton.setObjectName("itsFollowButton")
        self.fansButton = QtWidgets.QPushButton(self.showUserFrame)
        self.fansButton.setGeometry(QtCore.QRect(590, 40, 51, 30))
        self.fansButton.setObjectName("fansButton")
        self.blackListButton = QtWidgets.QPushButton(self.showUserFrame)
        self.blackListButton.setGeometry(QtCore.QRect(650, 40, 51, 30))
        self.blackListButton.setObjectName("blackListButton")
        self.friendButton = QtWidgets.QPushButton(self.showUserFrame)
        self.friendButton.setGeometry(QtCore.QRect(710, 40, 51, 30))
        self.friendButton.setObjectName("friendButton")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.userHeadLabel.setText(_translate("MainWindow", "TextLabel"))
        self.usernameLabel.setText(_translate("MainWindow", "TextLabel"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.followButton.setText(_translate("MainWindow", "关注"))
        self.collectionButton.setText(_translate("MainWindow", "收藏"))
        self.illustButton.setText(_translate("MainWindow", "作品集"))
        self.itsFollowButton.setText(_translate("MainWindow", "他关注"))
        self.fansButton.setText(_translate("MainWindow", "粉丝"))
        self.blackListButton.setText(_translate("MainWindow", "黑名单"))
        self.friendButton.setText(_translate("MainWindow", "好P友"))
