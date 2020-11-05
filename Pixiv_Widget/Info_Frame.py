#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PyQt5 import sip
from PyQt5.QtCore import QRect, QPropertyAnimation

from qtcreatorFile import info_frame_1
from PyQt5.QtWidgets import QFrame, QLabel

from .My_Label import my_label
from .Text_Scroll import text_scroll
from Pixiv_Thread.My_Thread import base_thread

import cgitb
cgitb.enable(format='text', logdir='log_file')
class info_frame(QFrame, info_frame_1.Ui_Frame):
    def __init__(self, parent, main, info={}):
        super(info_frame, self).__init__(parent)
        self.showDetail = False
        self.main = main
        self.info = info
        self.setupUi(self)
        authText_geometry = self.authText.geometry()
        self.authText.deleteLater()
        sip.delete(self.authText)
        self.authText = my_label(self, info={'tag': '', 'text':''})
        self.authText.setGeometry(authText_geometry)
        self.authText.setStyleSheet('color: rgb(255, 255, 255)')
        self.titleText.setStyleSheet('color: rgb(255, 255, 255)')
        self.text_scroll = text_scroll(self)
        self.text_scroll.click.connect(self.mouseReleaseEvent)
        self.setStyleSheet('background-color: rgb(32,32, 34)')

    def show_illust_detail(self):
        from PyQt5.Qt import QPropertyAnimation

        infoFrame_h_differ = 200  # 隐藏作品详情和展示时infoFrame之间的高度差
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
        self.animation.setEndValue(QRect(infoFrame_x, infoFrame_y - infoFrame_h_differ, infoFrame_w, infoFrame_h + infoFrame_h_differ))
        self.animation.setDuration(200)
        self.animation.finished.connect(change_animation_status)
        self.animation.start()
        self.animation_start = True
        self.showDetail = True
        return

    def create_illust_detail_panel(self, info):
        import os

        temp_path = self.info['temp_path']

        api = info['api']
        illust = info['illust']
        file_name = info['file_name']

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
            self.detail_labels[k].setStyleSheet('background-color: rgba(255, 255, 255, 0);color: white')
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

        if os.path.exists(f'{temp_path}/{file_name}'):
            print('user_head is exists.')
            self.load_user_head(
                info={"file_name": file_name, 'isSuccess': True, 'url': illust['user']['profile_image_urls']['medium'],
                      'api': api})
        else:
            self.baseThread = base_thread(self, api.cache_pic,
                                                     url=illust['user']['profile_image_urls']['medium'],
                                                     path=temp_path, file_name=file_name,
                                                     info={'file_name': file_name,
                                                           'url': illust['user']['profile_image_urls']['medium'],
                                                            'row': 1022, 'api': api})
            self.baseThread.finish.connect(self.load_user_head)
            self.baseThread.wait()
            self.baseThread.start()

    def load_user_head(self, info):
        from PyQt5.QtGui import QPixmap
        from PyQt5.QtCore import Qt
        import os

        temp_path = self.info['temp_path']
        timeout_pic = self.info['timeout_pic']
        
        label = self.user_pic_label
        url = info['url']
        file_name = info['file_name']
        api = info['api']


        if info['isSuccess']:
            file = f"{temp_path}/{file_name}"
        else:
            file = timeout_pic
        print(file)
        try:
            picture = QPixmap(file).scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if picture.isNull():
                try:
                    os.remove(file)
                except:
                    pass
                self.baseThread = base_thread(self, api.cache_pic, url=url, path=temp_path,
                                                         file_name=file_name,
                                                         info={'file_name': file_name, 'url': url, 'row': 1062, 'api': api})
                self.baseThread.finish.connect(self.load_user_head)
                self.baseThread.wait()
                self.baseThread.start()
                return
            label.setPixmap(picture)
        except (RuntimeError, KeyError, PermissionError) as e:
            pass

    def hide_illust_detail(self):
        infoFrame_h_differ = 200
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
            QRect(infoFrame_x, infoFrame_y + infoFrame_h_differ, infoFrame_w, infoFrame_h - infoFrame_h_differ))
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
    import sys

    app = QApplication(sys.argv)
    a = info_frame(None)
    a.text_scroll.setText(f'{"f"*1000}')
    a.show()
    sys.exit(app.exec_())