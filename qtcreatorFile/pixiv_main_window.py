# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtcreatorFile/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1257, 811)
        MainWindow.setIconSize(QtCore.QSize(32, 32))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.SmallFrame = QtWidgets.QFrame(self.centralWidget)
        self.SmallFrame.setGeometry(QtCore.QRect(120, 0, 1050, 731))
        self.SmallFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SmallFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SmallFrame.setObjectName("SmallFrame")
        self.bigPicScrollArea = QtWidgets.QScrollArea(self.SmallFrame)
        self.bigPicScrollArea.setGeometry(QtCore.QRect(0, 0, 1041, 731))
        self.bigPicScrollArea.setWidgetResizable(False)
        self.bigPicScrollArea.setObjectName("bigPicScrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 1017, 729))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.bigPicLabel = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.bigPicLabel.setGeometry(QtCore.QRect(0, 0, 1041, 611))
        self.bigPicLabel.setObjectName("bigPicLabel")
        self.bigPicScrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.DownloadPageScroll = QtWidgets.QTableView(self.SmallFrame)
        self.DownloadPageScroll.setGeometry(QtCore.QRect(0, 0, 1041, 731))
        self.DownloadPageScroll.setObjectName("DownloadPageScroll")
        self.tabWidget = QtWidgets.QTabWidget(self.SmallFrame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1041, 731))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.DownloadPageScroll.raise_()
        self.bigPicScrollArea.raise_()
        self.tabWidget.raise_()
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 120, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.login_user_pic_label = QtWidgets.QLabel(self.frame)
        self.login_user_pic_label.setGeometry(QtCore.QRect(35, 2, 50, 50))
        self.login_user_pic_label.setText("")
        self.login_user_pic_label.setObjectName("login_user_pic_label")
        self.usernameLabel = Username_Label(self.frame)
        self.usernameLabel.setGeometry(QtCore.QRect(0, 50, 120, 41))
        self.usernameLabel.setText("")
        self.usernameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.usernameLabel.setWordWrap(True)
        self.usernameLabel.setObjectName("usernameLabel")
        self.function_frame = QtWidgets.QFrame(self.centralWidget)
        self.function_frame.setGeometry(QtCore.QRect(0, 611, 120, 200))
        self.function_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.function_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.function_frame.setObjectName("function_frame")
        self.logoutButton = QtWidgets.QCommandLinkButton(self.function_frame)
        self.logoutButton.setGeometry(QtCore.QRect(0, 121, 121, 41))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/注销-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.logoutButton.setIcon(icon)
        self.logoutButton.setObjectName("logoutButton")
        self.showDownloadButton = QtWidgets.QCommandLinkButton(self.function_frame)
        self.showDownloadButton.setGeometry(QtCore.QRect(0, 80, 121, 41))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/下载-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showDownloadButton.setIcon(icon1)
        self.showDownloadButton.setObjectName("showDownloadButton")
        self.settingsButton = QtWidgets.QCommandLinkButton(self.function_frame)
        self.settingsButton.setGeometry(QtCore.QRect(0, 39, 121, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/设置-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settingsButton.setIcon(icon2)
        self.settingsButton.setObjectName("settingsButton")
        self.searchButton = QtWidgets.QCommandLinkButton(self.function_frame)
        self.searchButton.setGeometry(QtCore.QRect(0, -2, 121, 41))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/搜索-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton.setIcon(icon3)
        self.searchButton.setObjectName("searchButton")
        self.downloadTipsLabel = QtWidgets.QLabel(self.function_frame)
        self.downloadTipsLabel.setGeometry(QtCore.QRect(90, 90, 20, 20))
        self.downloadTipsLabel.setText("")
        self.downloadTipsLabel.setObjectName("downloadTipsLabel")
        self.aboutButton = QtWidgets.QCommandLinkButton(self.function_frame)
        self.aboutButton.setGeometry(QtCore.QRect(0, 160, 121, 41))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/关于.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon4)
        self.aboutButton.setObjectName("aboutButton")
        self.aboutButton.raise_()
        self.showDownloadButton.raise_()
        self.logoutButton.raise_()
        self.settingsButton.raise_()
        self.searchButton.raise_()
        self.downloadTipsLabel.raise_()
        self.cate_scrollArea = QtWidgets.QScrollArea(self.centralWidget)
        self.cate_scrollArea.setGeometry(QtCore.QRect(0, 91, 120, 522))
        self.cate_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cate_scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.cate_scrollArea.setWidgetResizable(False)
        self.cate_scrollArea.setObjectName("cate_scrollArea")
        self.cate_widget = QtWidgets.QWidget()
        self.cate_widget.setGeometry(QtCore.QRect(0, 0, 119, 519))
        self.cate_widget.setObjectName("cate_widget")
        self.weekOriginalButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.weekOriginalButton.setGeometry(QtCore.QRect(0, 287, 121, 41))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/正常-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.weekOriginalButton.setIcon(icon5)
        self.weekOriginalButton.setObjectName("weekOriginalButton")
        self.recommendButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.recommendButton.setGeometry(QtCore.QRect(0, 0, 121, 41))
        self.recommendButton.setIcon(icon5)
        self.recommendButton.setObjectName("recommendButton")
        self.dayMangaButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.dayMangaButton.setGeometry(QtCore.QRect(0, 164, 121, 41))
        self.dayMangaButton.setIcon(icon5)
        self.dayMangaButton.setObjectName("dayMangaButton")
        self.dayFemaleButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.dayFemaleButton.setGeometry(QtCore.QRect(0, 123, 121, 41))
        self.dayFemaleButton.setIcon(icon5)
        self.dayFemaleButton.setObjectName("dayFemaleButton")
        self.dayRookieButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.dayRookieButton.setGeometry(QtCore.QRect(0, 246, 121, 41))
        self.dayRookieButton.setIcon(icon5)
        self.dayRookieButton.setObjectName("dayRookieButton")
        self.monthButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.monthButton.setGeometry(QtCore.QRect(0, 328, 121, 41))
        self.monthButton.setIcon(icon5)
        self.monthButton.setObjectName("monthButton")
        self.R18Button = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.R18Button.setGeometry(QtCore.QRect(0, 369, 121, 41))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("qtcreatorFile/../RES/男女-p.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.R18Button.setIcon(icon6)
        self.R18Button.setObjectName("R18Button")
        self.dayMaleButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.dayMaleButton.setGeometry(QtCore.QRect(0, 82, 121, 41))
        self.dayMaleButton.setIcon(icon5)
        self.dayMaleButton.setObjectName("dayMaleButton")
        self.RankButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.RankButton.setGeometry(QtCore.QRect(0, 41, 121, 41))
        self.RankButton.setIcon(icon5)
        self.RankButton.setObjectName("RankButton")
        self.weekButton = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.weekButton.setGeometry(QtCore.QRect(0, 205, 121, 41))
        self.weekButton.setIcon(icon5)
        self.weekButton.setObjectName("weekButton")
        self.R18Button_male = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.R18Button_male.setGeometry(QtCore.QRect(0, 411, 121, 41))
        self.R18Button_male.setIcon(icon6)
        self.R18Button_male.setObjectName("R18Button_male")
        self.R18Button_female = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.R18Button_female.setGeometry(QtCore.QRect(0, 452, 121, 41))
        self.R18Button_female.setIcon(icon6)
        self.R18Button_female.setObjectName("R18Button_female")
        self.R18Button_week = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.R18Button_week.setGeometry(QtCore.QRect(0, 493, 121, 41))
        self.R18Button_week.setIcon(icon6)
        self.R18Button_week.setObjectName("R18Button_week")
        self.R18Button_week_G = QtWidgets.QCommandLinkButton(self.cate_widget)
        self.R18Button_week_G.setGeometry(QtCore.QRect(0, 534, 121, 41))
        self.R18Button_week_G.setIcon(icon6)
        self.R18Button_week_G.setObjectName("R18Button_week_G")
        self.cate_scrollArea.setWidget(self.cate_widget)
        self.frame.raise_()
        self.SmallFrame.raise_()
        self.function_frame.raise_()
        self.cate_scrollArea.raise_()
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.bigPicLabel.setText(_translate("MainWindow", "TextLabel"))
        self.logoutButton.setText(_translate("MainWindow", "注销"))
        self.showDownloadButton.setText(_translate("MainWindow", "下载"))
        self.settingsButton.setText(_translate("MainWindow", "设置"))
        self.searchButton.setText(_translate("MainWindow", "搜索"))
        self.aboutButton.setText(_translate("MainWindow", "关于"))
        self.weekOriginalButton.setText(_translate("MainWindow", "原创"))
        self.recommendButton.setText(_translate("MainWindow", "推荐"))
        self.dayMangaButton.setText(_translate("MainWindow", "漫画"))
        self.dayFemaleButton.setText(_translate("MainWindow", "女性"))
        self.dayRookieButton.setText(_translate("MainWindow", "新人"))
        self.monthButton.setText(_translate("MainWindow", "每月"))
        self.R18Button.setText(_translate("MainWindow", "R18"))
        self.dayMaleButton.setText(_translate("MainWindow", "男性"))
        self.RankButton.setText(_translate("MainWindow", "每日"))
        self.weekButton.setText(_translate("MainWindow", "每周"))
        self.R18Button_male.setText(_translate("MainWindow", "R18男"))
        self.R18Button_female.setText(_translate("MainWindow", "R18女"))
        self.R18Button_week.setText(_translate("MainWindow", "R18周"))
        self.R18Button_week_G.setText(_translate("MainWindow", "R18重"))
from Pixiv_Widget.My_Label import Username_Label
