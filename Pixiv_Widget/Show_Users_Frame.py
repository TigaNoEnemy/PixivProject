#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QPushButton
from PyQt5.QtCore import pyqtSignal
import os

from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.Clickable_Label import clickable_label
from Pixiv_Widget.My_Widget import Show_User_Illust_Label
from Pixiv_Widget.My_Widget import Show_Head_Label


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


class show_users_frame(QFrame):
    """docstring for show_users_frame"""
    click = pyqtSignal(dict)

    def __init__(self, parent, info):
        super(show_users_frame, self).__init__(parent)
        self.info = info
        self.check_info()
        self.setupUi()
        self.my_set()
        self.action_to_command()

    def check_info(self):
        key = ['user_preview', 'api', 'loading_gif', 'timeout_pic', 'temp_path', 'save_path', 'has_r18', 'no_h', 'app']
        need_key = []
        need_not_key = []
        for i in self.info:
            if i not in key:
                need_not_key.append(i)
        for i in key:
            if i not in self.info:
                need_key.append(i)
        if need_key or need_not_key:
            raise KeyError(f"small_pic_frame doesn't need {need_not_key} and need {need_key}")
    
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
                'temp_path': self.info['temp_path'], 
                'user_id': user['user']['id'], 
                'api': self.info['api'],
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
        api = self.info['api']
        temp_path = self.info['temp_path']
        has_r18 = self.info['has_r18']
        no_h = self.info['no_h']

        username = user['user']['name']
        user_head_url = user['user']['profile_image_urls']['medium']
        user_id = user['user']['id']
        illusts = user['illusts']
        temp_file_name = f"user_{user_id}"

        self.usernameLabel.setText(username)
        self.usernameLabel.adjustSize()

        file = f"{temp_path}/{temp_file_name}"
        info = {
            'label': self.userHeadLabel, 
            'temp_file_name': f"user_{user_id}", 
            'temp_path': temp_path, 
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

            info = {'url': url, 'title': title, 'illust_id': temp_file_name, 'temp_path': temp_path, 'api': api, 'illust': illusts[i], 'has_r18': has_r18, 'no_h': no_h}    # illust 是为了点击时传递给Main_Pixiv.main_pixiv.show_big_pic
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
            # gif = QMovie(loading_gif)
            # self.label[i].setMovie(gif)
            # gif.start()
            # info = {
            #     'label': self.label[i], 
            #     'temp_file_name': temp_file_name, 
            #     'temp_path': temp_path, 
            #     'url': url, 
            #     'just_show': just_show,
            #     'self': 'small'
            #     }
            # if not os.path.exists(file):
            #     self.get_illust_thread[i] = base_thread(self, api.cache_pic, info=info, url=url, path=temp_path, file_name=temp_file_name)
            #     self.get_illust_thread[i].finish.connect(self.load_complete_pic)
            #     self.get_illust_thread[i].wait()
            #     self.get_illust_thread[i].start()
            # else:
            #     info['isSuccess'] = True
            #     self.load_complete_pic(info)

    def load_complete_pic(self, result):
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt

        timeout_pic = self.info['timeout_pic']
        no_h = self.info['no_h']

        label = result['label']
        temp_path = result['temp_path']
        temp_file_name = result['temp_file_name']
        url = result['url']
        isSuccess = result['isSuccess']
        just_show = result.get('just_show', True)

        file = f'{temp_path}/{temp_file_name}'
        if not isSuccess:
            file = timeout_pic

        if not just_show:
            file = no_h

        picture = QPixmap(file).scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        label.setPixmap(picture)

        info = {'url': url, 'temp_file_name': temp_file_name, 'temp_path': temp_path, 'label': label}
        try:
            label.info.update(info)
            label.double_click.connect(self.force_reload)
        except:
            pass

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
        api = self.info['api']

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

        self.user_action = base_thread(self, api.follow_user, user_id=user_id, publicity=publicity)
        self.user_action.finish.connect(seeIfSuccess)
        self.user_action.wait()
        self.user_action.start()

    def disfollow_user(self):
        from PyQt5 import sip

        user = self.info['user_preview']
        api = self.info['api']

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

        self.user_action = base_thread(self, api.disfollow_user, user_id=user_id, publicity='public')
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

        mode = {}
        mode['user_id'] = user_id
        mode['restrict'] = 'public'
        mode['offset'] = None
        mode['Thread'] = """base_thread(self, self.api.user_following,
            info={'title': title},
            user_id=%s,
            restrict='public',
            offset=None)"""%user_id
        title = f"{username}的关注"
        
        app.search_user(_mode=mode, title=title, isSearch=False)

    def user_follower(self):
        # 用户粉丝
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        mode = {}
        mode['user_id'] = user_id
        mode['Thread'] = """base_thread(self,
            self.api.user_follower,
            info={'title': title},
            user_id=%s,
            filter='for_ios',
            offset=None,
            )"""%user_id
        title = f"{username}的粉丝"
        app.search_user(_mode=mode, title=title, isSearch=False)

    def user_black_list(self, arg):
        pass

    def user_friend(self, arg):
        user = self.info['user_preview']
        app = self.info['app']

        user_id = user['user']['id']
        username = user['user']['name']

        mode = {}
        mode['user_id'] = user_id
        mode['Thread'] = """base_thread(self,
        self.api.user_mypixiv,
        info={'title': title},
        user_id=%s,
        offset=None
        )"""%user_id
        title = f"{username}的好友"
        app.search_user(_mode=mode, title=title, isSearch=False)

    def force_reload(self, info):
        from PyQt5.QtGui import QMovie

        def try_pop(_info):
            temp_file_name = _info['temp_file_name']
            try:
                self.reload_thread.pop(temp_file_name)
            except KeyError:
                pass

        if not hasattr(self, 'reload_thread'):
            self.reload_thread = {}

        label = info['label']
        url = info['url']
        temp_path = info['temp_path']
        temp_file_name = info['temp_file_name']
        api = self.info['api']
        loading_gif = self.info['loading_gif']

        file = f"{temp_path}/{temp_file_name}"

        try:
            os.remove(file)
        except:
            pass

        gif = QMovie(loading_gif)
        label.setMovie(gif)
        gif.start()

        self.reload_thread[temp_file_name] = base_thread(self, api.cache_pic, info={'label': label, 'temp_path': temp_path, 'temp_file_name': temp_file_name, 'url': url}, url=url, path=temp_path, file_name=temp_file_name)
        self.reload_thread[temp_file_name].finish.connect(self.load_complete_pic)
        self.reload_thread[temp_file_name].finish.connect(try_pop)
        self.reload_thread[temp_file_name].wait()
        self.reload_thread[temp_file_name].start()

    def show_big_pic(self, info):
        self.click.emit(info)