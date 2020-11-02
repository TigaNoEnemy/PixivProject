#!/usr/bin/env python3
import sys
sys.path.append('.')
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from datetime import datetime

from Pixiv_Thread.My_Thread import base_thread
from qtcreatorFile.oneComment import Ui_oneComment


class One_Comment(QFrame, Ui_oneComment):
    """info包含整个comment（dict）、api、temp_path"""
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
        print(self.comment_text.verticalScrollBar().isVisible(), '='*90)
        # while self.comment_text.verticalScrollBar().isVisible():
        #     self.comment_text.resize(self.comment_text.width(), self.comment_text.height()+2)
        #     if self.self.comment_text.height() >= 300:
        #         break

    def download_user_pic(self):
        user_head_url = self.info['user']['profile_image_urls']['medium']
        uid = self.info['user']['id']
        api = self.info['api']
        temp_path = self.info['temp_path']

        file_name = f"user_{uid}_pic"
        load_user_head_thread = base_thread(self, api.cache_pic, url=user_head_url, file_name=file_name,
                                           path=temp_path, info={'file_name': file_name, 'url': user_head_url, 'temp_path': temp_path})
        load_user_head_thread.finish.connect(self.load_user_head)
        load_user_head_thread.wait()
        load_user_head_thread.start()

    def load_user_head(self, info):
        api = self.info['api']

        user_head_url = info['url']
        file_name = info['file_name']
        temp_path = info['temp_path']

        file = f"{temp_path}/{file_name}"

        user_head = QPixmap(file)
        if user_head.isNull():
            try:
                os.remove(file)
            except:
                pass
            load_user_head_thread = base_thread(self, api.cache_pic, url=user_head_url, file_name=file_name,
                                           path=temp_path, info={'file_name': file_name, 'url': user_head_url, 'temp_path': temp_path})
            load_user_head_thread.finish.connect(self.load_user_head)
            load_user_head_thread.wait()
            load_user_head_thread.start()

        else:
            user_head = user_head.scaled(self.user_pic_label.width(), self.user_pic_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.user_pic_label.setPixmap(user_head)


        

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
    api.auth(refresh_token=info['token'])

    data = api.illust_comments(85256262)

    temp_path = l_cfg.temp_path

    info = data['comments'][0]
    info['comment'] = '\n'.join(info['comment'])
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

    