#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QCursor
import os

from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.Clickable_Label import clickable_label
from Pixiv_Widget.My_Widget import Show_User_Illust_Label
from Pixiv_Widget.My_Widget import Show_Head_Label
from Pixiv_Api.My_Api import my_api
from utils.Project_Setting import setting


import cgitb
cgitb.enable(format='text', logdir='log_file')
class my_button(QPushButton):
    """docstring for my_button"""
    click = pyqtSignal(dict)
    def __init__(self, parent, arg={}):
        super(my_button, self).__init__(parent)
        self.arg = arg
        self.clickable = True

    def mouseReleaseEvent(self, qevent):
        super(my_button, self).mouseReleaseEvent(qevent)
        if qevent.button() == 1 and self.arg and self.clickable:
            self.click.emit(self.arg)

    def setClickable(self, isClickable):
        self.clickable = isClickable

    def enterEvent(self, qevent):
        self.setCursor(QCursor(Qt.PointingHandCursor))


class show_users_frame(QFrame):
    """docstring for show_users_frame"""
    click = pyqtSignal(dict)

    def __init__(self, parent, info):
        super(show_users_frame, self).__init__(parent)
        self.info = info
        self.api = my_api()
        self.cfg = setting()
        self.check_info()
        self.setupUi()
        self.my_set()
        self.action_to_command()

    def check_info(self):
        key = ['user_preview', 'app']
    
    def setupUi(self):
        from PyQt5.QtCore import QRect, QMetaObject
        from PyQt5.QtWidgets import QLabel
        user = self.info['user_preview']

        user_id = user['user']['id']

        self.setObjectName("show_users_frame")
        self.setEnabled(True)
        self.resize(1257, 811)
        #     key = ['url', 'temp_path', 'user_id', 'api']
        user = self.info['user_preview']
        info = {
                'url': user['user']['profile_image_urls']['medium'], 
                'user_id': user['user']['id'], 
                }
        self.userHeadLabel = Show_Head_Label(self, info=info)
        self.userHeadLabel.setGeometry(QRect(30, 20, 50, 50))
        #self.userHeadLabel.setStyleSheet("background-color: rgb(255, 228, 249);")
        self.userHeadLabel.setObjectName("userHeadLabel")
        self.userHeadLabel.get_head()

        self.usernameLabel = clickable_label(self, info={'user_id': user_id})
        self.usernameLabel.setGeometry(QRect(90, 50, 171, 20))
        #self.usernameLabel.setStyleSheet("background-color: rgb(175, 255, 246);")
        self.usernameLabel.setObjectName("usernameLabel")
        self.followButton = my_button(self)
        self.followButton.setGeometry(QRect(350, 40, 51, 30))
        self.followButton.setObjectName("followButton")
        self.collectionButton = my_button(self)
        self.collectionButton.setGeometry(QRect(410, 40, 51, 30))
        self.collectionButton.setObjectName("collectionButton")
        self.illustButton = my_button(self)
        self.illustButton.setGeometry(QRect(470, 40, 51, 30))
        self.illustButton.setObjectName("illustButton")
        self.itsFollowButton = my_button(self)
        self.itsFollowButton.setGeometry(QRect(530, 40, 51, 30))
        self.itsFollowButton.setObjectName("itsFollowButton")
        self.fansButton = my_button(self)
        self.fansButton.setGeometry(QRect(590, 40, 51, 30))
        self.fansButton.setObjectName("fansButton")
        self.blackListButton = my_button(self)
        self.blackListButton.setGeometry(QRect(650, 40, 51, 30))
        self.blackListButton.setObjectName("blackListButton")
        self.friendButton = my_button(self)
        self.friendButton.setGeometry(QRect(710, 40, 51, 30))
        self.friendButton.setObjectName("friendButton")

        self.show()
        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        from PyQt5.QtCore import QCoreApplication

        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.userHeadLabel.setText(_translate("self", ""))
        self.usernameLabel.setText(_translate("self", ""))
        self.followButton.setText(_translate("self", "关注"))
        self.collectionButton.setText(_translate("self", "收藏"))
        self.illustButton.setText(_translate("self", "作品集"))
        self.itsFollowButton.setText(_translate("self", "他关注"))
        self.fansButton.setText(_translate("self", "粉丝"))
        self.blackListButton.setText(_translate("self", "黑名单"))
        self.friendButton.setText(_translate("self", "好P友"))

    def my_set(self):
        from PyQt5.QtGui import QMovie
        from PyQt5.QtCore import QRect, Qt

        user = self.info['user_preview']

        username = user['user']['name']
        user_head_url = user['user']['profile_image_urls']['medium']
        user_id = user['user']['id']
        illusts = user['illusts']
        temp_file_name = f"user_{user_id}"

        self.usernameLabel.setText(username)
        self.usernameLabel.adjustSize()

        file = f"{self.cfg.temp_path}/{temp_file_name}"
        info = {
            'label': self.userHeadLabel, 
            'temp_file_name': f"user_{user_id}", 
            'url': user_head_url
            }
        # if not os.path.exists(file):
        #     self.userHeadThread = base_thread(self, api.cache_pic, url=user_head_url, path=temp_path, file_name=temp_file_name, info=info)
        #     self.userHeadThread.finish.connect(self.load_complete_pic)
        #     self.userHeadThread.wait()
        #     self.userHeadThread.start()
        # else:
        #     info['isSuccess'] = True
        #     self.load_complete_pic(info)

        self.label = {}
        #self.get_illust_thread = {}
        for i in range(len(illusts)):
            url = illusts[i]['image_urls']['square_medium']
            title = illusts[i]['title']
            if 'R-18' in str(illusts[i]['tags']):
                temp_file_name = f"{illusts[i]['id']}_r18"
            else:
                temp_file_name = illusts[i]['id']
            #file = f"{temp_path}/{temp_file_name}"
            #just_show = True
            # if not has_r18 and 'R-18' in str(illusts[i]['tags']):
            #     file = no_h
            #     just_show = False

            info = {'url': url, 'title': title, 'illust_id': temp_file_name, 'illust': illusts[i]}    # illust 是为了点击时传递给Main_Pixiv.main_pixiv.show_big_pic
            self.label[i] = Show_User_Illust_Label(self, info=info)
            self.label[i].set_is_loading(True)
            self.label[i].get_relate_pic()
            self.label[i].click.connect(self.show_big_pic)
            self.label[i].setGeometry(QRect(30+i*250, 110, 234, 234))
            self.label[i].set_original_geometry(30+i*250, 110, 234, 234)
            self.label[i].setAlignment(Qt.AlignCenter)
            self.label[i].click.connect(self.show_big_pic)
            self.label[i].setObjectName("label")
            self.label[i].show()

    def load_complete_pic(self, result):
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt

        label = result['label']
        temp_file_name = result['temp_file_name']
        url = result['url']
        isSuccess = result['isSuccess']
        just_show = result.get('just_show', True)

        file = f'{self.cfg.temp_path}/{temp_file_name}'
        if not isSuccess:
            file = self.cfg.timeout_pic

        if not just_show:
            file = self.cfg.no_h

        picture = QPixmap(file).scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(picture)

    def action_to_command(self):
        user = self.info['user_preview']

        user_id = user['user']['id']
        is_followed = user['user']['is_followed']

        if is_followed:
            self.followButton.clicked.connect(self.disfollow_user)
            self.followButton.setText('取关')
        else:
            self.followButton.clicked.connect(self.follow_user)

        self.collectionButton.clicked.connect(self.user_bookmarks_illust)
        self.illustButton.clicked.connect(self.user_illusts)
        self.itsFollowButton.clicked.connect(self.user_following)
        self.fansButton.clicked.connect(self.user_follower)
        self.blackListButton.clicked.connect(self.user_black_list)
        self.friendButton.clicked.connect(self.user_friend)

    def follow_user(self):
        from PyQt5 import sip

        user = self.info['user_preview']

        self.followButton.setClickable(False)

        user_id = user['user']['id']

        publicity = 'public'
        def seeIfSuccess(info):
            if info['status'] == 'success':
                self.followButton.setText('取关')
                self.followButton.disconnect()
                self.followButton.click.connect(self.disfollow_user)
            self.user_action.deleteLater()
            sip.delete(self.user_action)
            del self.user_action
            self.followButton.setClickable(True)

        self.user_action = base_thread(self, self.api.follow_user, user_id=user_id, publicity=publicity)
        self.user_action.finish.connect(seeIfSuccess)
        self.user_action.wait()
        self.user_action.start()

    def disfollow_user(self):
        from PyQt5 import sip

        user = self.info['user_preview']

        self.followButton.setClickable(False)
        user_id = user['user']['id']

        def seeIfSuccess(info):
            if info['status'] == 'success':
                self.followButton.setText('关注')
                self.followButton.disconnect()
                self.followButton.click.connect(self.follow_user)
            self.user_action.deleteLater()
            sip.delete(self.user_action)
            del self.user_action
            self.followButton.setClickable(True)

        self.user_action = base_thread(self, self.api.disfollow_user, user_id=user_id, publicity='public')
        self.user_action.finish.connect(seeIfSuccess)
        self.user_action.wait()
        self.user_action.start()

    def user_bookmarks_illust(self):
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        mode = {}
        mode['user_id'] = user_id
        mode['restrict'] = 'public'
        mode['filter'] = 'for_ios'
        mode['max_bookmark_id'] = None
        mode['tag'] = None
        title = f"{username}的收藏"
        app.show_pic(_mode=mode, title=title, flag='收藏作品')

    def user_illusts(self):
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        mode = {}
        mode['user_id'] = user_id
        mode['type'] = 'illust'
        mode['filter'] = 'for_ios'
        mode['offset'] = None
        title = f"画师：{username}"
        app.show_pic(_mode=mode, title=title, flag='用户作品')


    def user_following(self, arg):
        # 用关注
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        title = f"{username}的关注"

        mode = {}
        mode['user_id'] = user_id
        mode['restrict'] = 'public'
        mode['offset'] = None
        mode['Thread'] = base_thread(
            self, 
            self.api.user_following,
            info={'title': title},
            user_id=user_id,
            restrict='public',
            offset=None
            )
        
        
        app.search_user(_mode=mode, title=title, isSearch=False)

    def user_follower(self):
        # 用户粉丝
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        title = f"{username}的粉丝"

        mode = {}
        mode['user_id'] = user_id
        mode['Thread'] = base_thread(
            self,
            self.api.user_follower,
            info={'title': title},
            user_id=user_id,
            filter='for_ios',
            offset=None,
            )
        
        app.search_user(_mode=mode, title=title, isSearch=False)

    def user_black_list(self, arg):
        pass

    def user_friend(self, arg):
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        title = f"{username}的好友"

        mode = {}
        mode['user_id'] = user_id
        mode['Thread'] = base_thread(
            self,
            self.api.user_mypixiv,
            info={'title': title},
            user_id=user_id,
            offset=None
            )
        
        app.search_user(_mode=mode, title=title, isSearch=False)

    def show_big_pic(self, info):
        self.click.emit(info)