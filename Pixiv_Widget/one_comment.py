#!/usr/bin/env python3
import sys
sys.path.append('.')
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime

from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.My_Widget import Show_Head_Label
from qtcreatorFile.oneComment import Ui_oneComment

import cgitb
cgitb.enable(format='text', logdir='log_file')
class One_Comment(QFrame, Ui_oneComment):
    """info包含整个comment（dict）"""
    def __init__(self, parent, info, *args, **kwargs):
        super(One_Comment, self).__init__(parent, *args, **kwargs)
        self.info = info
        self.setupUi(self)
        self.load_comment()
        self.download_user_pic()

    def load_comment(self):
        comment = self.info['comment']
        user_name = self.info['user']['name']
        comment_time = self.info['date']

        date, _time = comment_time.split('T')
        if '+' in _time:
            time, tzone = _time.split('+')
            comment_time = f"{date} {time} +{tzone}"
        elif '-' in _time:
            time, tzone = _time.split('-')
            comment_time = f"{date} {time} -{tzone}"

        self.user_name_label.setText(user_name)
        self.time_label.setText(comment_time)
        self.time_label.adjustSize()
        self.comment_text.insertPlainText(comment)
        #self.comment_text.resize(self.comment_text.width(), 23)
        # print(self.comment_text.verticalScrollBar().isVisible(), '='*90)
        # while self.comment_text.verticalScrollBar().isVisible():
        #     self.comment_text.resize(self.comment_text.width(), self.comment_text.height()+2)
        #     if self.self.comment_text.height() >= 300:
        #         break

    def download_user_pic(self):
        user_head_url = self.info['user']['profile_image_urls']['medium']
        uid = self.info['user']['id']

        self.user_pic_label.info = {'url': user_head_url, 'user_id': uid}
        self.user_pic_label.set_is_loading(True)
        self.user_pic_label.get_head()

if __name__ == '__main__':
    from utils.Process_Token import login_info_parser
    from Pixiv_Api.My_Api import my_api
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from utils.Project_Setting import setting

    l_cfg = setting()

    cfg = login_info_parser()
    info = cfg.get_token()

    api = my_api()
    api.hosts = api.require_appapi_hosts('public-api.secure.pixiv.net')
    api.pximg = api.require_appapi_hosts('i.pximg.net')
    api.default_head = api.require_appapi_hosts('s.pximg.net')
    api.auth(refresh_token=info['token'])

    data = api.illust_comments(85256262)

    temp_path = l_cfg.temp_path

    info = data['comments'][0]
    #info['comment'] = '\n'.join(info['comment'])
    info.update({'temp_path': temp_path, 'api': api})

    app = QApplication(sys.argv)
    m = QMainWindow()
    o = One_Comment(m, info=info)
    o.move(0, 0)
    m.resize(o.width(), o.height())
    m.show()
    # from prettyprinter import cpprint
    # cpprint(data)
    sys.exit(app.exec_())

    