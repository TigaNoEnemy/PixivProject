#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5 import sip
from PyQt5.QtCore import QRect, QPropertyAnimation
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame, QLabel

import sys
sys.path.append('.')
from qtcreatorFile import info_frame_1
from Pixiv_Widget.My_Label import my_label
from Pixiv_Thread.My_Thread import base_thread

import cgitb
cgitb.enable(format='text', logdir='log_file')
class info_frame(QFrame, info_frame_1.Ui_Frame):
    infoFrame_h_differ = 200    # 隐藏作品详情和展示时infoFrame之间的高度差
    def __init__(self, parent=None, main=None, info={}):
        super(info_frame, self).__init__(parent)
        self.showDetail = False
        self.main = main
        self.info = info
        self.setupUi(self)
        # authText_geometry = self.authText.geometry()
        # self.authText.deleteLater()
        # sip.delete(self.authText)
        self.authText.info={'tag': '', 'text':''}
        # self.authText.setGeometry(authText_geometry)
        # self.authText.setStyleSheet('color: rgb(255, 255, 255)')
        # self.titleText.setStyleSheet('color: rgb(255, 255, 255)')
        # self.text_scroll = text_scroll(self)
        # print(self.text_scroll.pos(), self.text_scroll.size())
        self.text_scroll.click.connect(self.mouseReleaseEvent)
        # self.setStyleSheet('background-color: rgb(32,32, 34)')
        self.original_height = 0

    def show_illust_detail(self):
        from PyQt5.Qt import QPropertyAnimation
        if hasattr(self, 'animation'):
            if self.animation_start:
                return
            try:
                self.animation.deleteLater()
                sip.delete(self.animation)
            except:
                pass

        def change_animation_status():
            self.animation_start = False

        infoFrame_x = self.x()
        infoFrame_y = self.y()
        infoFrame_w = self.width()
        infoFrame_h = self.height()

        self.animation = QPropertyAnimation(self)
        self.animation.setPropertyName(b'geometry')
        self.animation.setTargetObject(self)
        self.animation.setStartValue(QRect(infoFrame_x, infoFrame_y, infoFrame_w, infoFrame_h))
        self.animation.setEndValue(QRect(infoFrame_x, infoFrame_y - self.infoFrame_h_differ, infoFrame_w, infoFrame_h + self.infoFrame_h_differ))
        self.animation.setDuration(200)
        self.animation.finished.connect(change_animation_status)
        self.animation.start()
        self.animation_start = True
        self.showDetail = True
        return

    def create_illust_detail_panel(self, info):
        self.user_pic_label.set_is_loading(True)

        import os

        illust = info['illust']

        right_label_w = 481  # 右边的作品详情，关于时间之类的
        label_h = 24
        right_label_x = 490
        if hasattr(self, 'detail_labels'):
            for j in self.detail_labels:
                self.detail_labels[j].deleteLater()
                sip.delete(self.detail_labels[j])

        if hasattr(self, 'animation'):
            try:
                self.animation.deleteLater()
                sip.delete(self.animation)
            except:
                pass

        self.detail_labels = {}
        self.detail_labels["create_date"] = QLabel(self)
        self.detail_labels["create_date"].setText(f"create_date: {illust['create_date']}")
        self.detail_labels['create_date'].setGeometry(QRect(right_label_x, 100 + 0 * 30, right_label_w, label_h))

        n = 0
        for j in illust['tags']:
            tag = j['name']
            if not j["translated_name"]:
                translated_name = ''
            else:
                translated_name = j["translated_name"]
            if n > 4:
                label_x = 240
                m = n - 5  # 一列可以有5行标签
            else:
                label_x = 0
                m = n

            text = f'{j["name"]}:{translated_name}'.rstrip(":")
            length = len(text)
            # 字符串长度大于20则对半折
            if length > 20:
                half_length = int(length / 2)
                text = f"{text[:half_length]}<br>{text[half_length:]}"
                tag_label_w = half_length * 12
            else:
                tag_label_w = length * 12

            self.detail_labels[text] = my_label(self, info={'text': text, 'tag': tag})
            self.detail_labels[text].setText(text)
            self.detail_labels[text].setGeometry(QRect(label_x, 100 + 35 * m, tag_label_w, label_h))

            self.detail_labels[text].clicked.connect(
                lambda x: self.main.search_illust(x, search_target='exact_match_for_tags'))
            self.detail_labels[text].setToolTip(f'原文：{j["name"]}\n翻译：{j["translated_name"]}')
            self.detail_labels[text].adjustSize()
            n += 1

        self.detail_labels['pic_size'] = QLabel(self)
        self.detail_labels['pic_size'].setText(f"size: {illust['width']}x{illust['height']}")
        self.detail_labels['pic_size'].setGeometry(QRect(right_label_x, 100 + 1 * 30, right_label_w, label_h))

        self.detail_labels['total_view'] = QLabel(self)
        self.detail_labels['total_view'].setText(f"total_view: {illust['total_view']}")
        self.detail_labels['total_view'].setGeometry(QRect(right_label_x, 100 + 2 * 30, right_label_w, label_h))

        self.detail_labels['total_bookmarks'] = QLabel(self)
        self.detail_labels['total_bookmarks'].setText(f"total_bookmarks: {illust['total_bookmarks']}")
        self.detail_labels['total_bookmarks'].setGeometry(QRect(right_label_x, 100 + 3 * 30, right_label_w, label_h))

        self.detail_labels['illust_id'] = QLabel(self)
        self.detail_labels['illust_id'].setText(f"illust_id: {illust['id']}")
        self.detail_labels['illust_id'].setGeometry(QRect(right_label_x, 100 + 4 * 30, right_label_w, label_h))

        for k in self.detail_labels:
            #self.detail_labels[k].setStyleSheet('background-color: rgba(255, 255, 255, 0);color: white')
            self.detail_labels[k].setWordWrap(True)
            self.detail_labels[k].show()

        self.saveButton.disconnect()
        self.saveButton.clicked.connect(lambda: self.main.saveOriginalPic(illust))
        self.moreButton.setText('返回')
        self.moreButton.disconnect()
        self.moreButton.clicked.connect(lambda: self.main.returnSmallPic())

        self.titleText.setText(illust["title"])
        self.authText.setText(f'画师：{illust["user"]["name"]}')
        self.authText.info = {'tag': illust["user"]["name"], 'text': f'画师：{illust["user"]["name"]}'}

        try:
            self.authText.disconnect()
        except:
            pass
        self.authText.clicked.connect(self.main.simulateSearch)
        self.authText.adjustSize()

        self.text_scroll.clear()
        self.text_scroll.setText(illust['caption'])

        self.user_pic_label.info = {'user_id': illust['user']['id'],'url': illust['user']['profile_image_urls']['medium']}
        self.user_pic_label.get_head()

    def hide_illust_detail(self):
        if hasattr(self, 'animation'):
            if self.animation_start:
                return
            try:
                self.animation.deleteLater()
                sip.delete(self.animation)
            except:
                pass

        def change_animation_status():
            self.animation_start = False

        infoFrame_x = self.x()
        infoFrame_y = self.y()
        infoFrame_w = self.width()
        infoFrame_h = self.height()
        # self.infoFrame.move(infoFrame_x, infoFrame_y+180)
        self.animation = QPropertyAnimation(self)
        self.animation.setPropertyName(b'geometry')
        self.animation.setTargetObject(self)
        self.animation.setStartValue(QRect(infoFrame_x, infoFrame_y, infoFrame_w, infoFrame_h))
        self.animation.setEndValue(
            QRect(infoFrame_x, infoFrame_y + self.infoFrame_h_differ, infoFrame_w, infoFrame_h - self.infoFrame_h_differ))
        self.animation.setDuration(200)
        self.animation.finished.connect(change_animation_status)
        self.animation.start()
        self.animation_start = True
        self.showDetail = False

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1 and self.saveButton.isVisible():
            if self.showDetail:
                self.hide_illust_detail()
            else:
                self.show_illust_detail()

    def detail_is_show(self):
        return self.showDetail

    def set_original_height(self, v):
        self.original_height = v

    def resizeEvent(self, qevent):
        width = self.width()
        text_scroll_w = width - 520
        text_scroll_new_x = (width - text_scroll_w) // 2
        self.text_scroll.setGeometry(text_scroll_new_x, 0, text_scroll_w, 81)
        moreButton_y = self.moreButton.y()
        self.moreButton.move(width - 91, moreButton_y)
        self.escapeDownloadPageButton.move(width - 91, moreButton_y)

        self.saveButton.move(width - 181, moreButton_y)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from utils.Process_Token import login_info_parser
    from Pixiv_Api.My_Api import my_api

    class temp_class:
        def search_illust(self, x, search_target='exact_match_for_tags'):
            pass
        def saveOriginalPic(self, x):
            pass
        def returnSmallPic(self):
            pass
        def simulateSearch(self):
            pass

    cfg = login_info_parser()
    info = cfg.get_token()

    l = my_api()
    l.require_appapi_hosts('public-api.secure.pixiv.net')
    print(0)
    l.auth(refresh_token=info['token'])
    illust = {'id': 56232434, 'title': 'リィネ', 'type': 'illust', 'image_urls': {'square_medium': 'https://i.pximg.net/c/540x540_10_webp/img-master/img/2016/04/07/07/36/15/56232434_p0_square1200.jpg', 'medium': 'https://i.pximg.net/c/540x540_70/img-master/img/2016/04/07/07/36/15/56232434_p0_master1200.jpg', 'large': 'https://i.pximg.net/c/600x1200_90_webp/img-master/img/2016/04/07/07/36/15/56232434_p0_master1200.jpg'}, 'caption': 'ちょっとだけお世話になったマギアブレイクというアプリが閉じたそうです。<br />４月、、、新しい何かが始まるかと思えば終わるものもあるんですね。<br />とりあえずリィネちゃんお疲れ様でした＾＾', 'restrict': 0, 'user': {'id': 1652353, 'name': 'まとけち', 'account': 'aria155-aqua', 'profile_image_urls': {'medium': 'https://i.pximg.net/user-profile/img/2019/03/11/22/48/45/15510276_e3b1036f8dc5a8c3364f7716991893db_170.jpg'}, 'is_followed': False}, 'tags': [{'name': 'マギアブレイク', 'translated_name': None}, {'name': 'リィネ', 'translated_name': None}, {'name': '超破壊!!バルバロッサ', 'translated_name': None}], 'tools': ['Photoshop'], 'create_date': '2016-04-07T07:36:15+09:00', 'page_count': 1, 'width': 800, 'height': 1107, 'sanity_level': 2, 'x_restrict': 0, 'series': None, 'meta_single_page': {'original_image_url': 'https://i.pximg.net/img-original/img/2016/04/07/07/36/15/56232434_p0.png'}, 'meta_pages': [], 'total_view': 11377, 'total_bookmarks': 624, 'is_bookmarked': False, 'visible': True, 'is_muted': False}

    #info = {"illust": illust, "api": l}
    info = {'temp_path': '.'}
    m = temp_class()
    app = QApplication(sys.argv)
    a = info_frame(info=info, main=m)
    a.create_illust_detail_panel(info={"illust": illust, "api": l})
    #a.text_scroll.setText(f'{"f"*1000}')
    a.show()
    print(a.parent())
    sys.exit(app.exec_())