#!/usr/bin/env python3
import sys
sys.path.append('.')
import os
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QTimer
import math

from qtcreatorFile.illust_relate import Ui_illust_relate
from Pixiv_Widget.Clickable_Label import clickable_label
from Pixiv_Widget.My_Label import Largable_Label
from Pixiv_Widget.My_Widget import Illust_Relate_Pic_Label
from Pixiv_Thread.My_Thread import base_thread

import cgitb
cgitb.enable(format='text', logdir='log_file')
class Illust_Relate(QFrame, Ui_illust_relate):
    one_label_is_clicked =  pyqtSignal(dict)
    loading_timer_start_num = 5

    # 加载相关作品的控件
    def __init__(self, parent, info, *args, **kwargs):
        # info 需要 temp_path, illust_id, api, has_r18, no_h
        super(Illust_Relate, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.resize(620+24, 744+24)
        self.info = info
        
        self.pic_num = 1    # 记录已加载多少张图

        # 下载相关图资料时的动作所需的配置
        self.is_loading = True
        self.rotate = 90
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.change_rotate)

        self.load_time = 0 # 请求相关图资料次数
        self.get_relate()
        ###

    def change_rotate(self):
        self.rotate += 1.5
        
    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF
        super(Illust_Relate, self).paintEvent(qevent)

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = (width - 50)//2
            load_y = 50

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, 50, 50)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x+10, load_y+10, 30, 30), -self.rotate*16, -90*16)# 画圆环, 进度条

            font = QFont('MicroSoft YaHei', 12, QFont.Bold, False)
            painter.setFont(font)
            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            painter.setPen(pen)
            font_width = painter.fontMetrics().width(str(self.load_time))
            font_height = painter.fontMetrics().height()
            painter.drawText((width-font_width)//2+1, 50*1.65, str(self.load_time))
        else:
            if self.loading_timer.isActive():
                self.loading_timer.stop()

        self.update()

    def get_relate(self):
        self.load_time += 1
        if not self.loading_timer.isActive():
            self.loading_timer.start(self.loading_timer_start_num)

        api = self.info['api']
        temp_path = self.info['temp_path']
        illust_id = self.info['illust_id']#['id']    # 获取相关性的作品id

        self.illust_thread = base_thread(self, api.illust_related, illust_id=illust_id)
        self.illust_thread.finish.connect(self.load_related_illust)
        self.illust_thread.wait()
        self.illust_thread.start()

    def load_related_illust(self, info):
        if info.get('ERROR', False):
            self.get_relate()

        else:
            self.is_loading = False
            illusts = info['illusts']

            temp_path = self.info['temp_path']
            api = self.info['api']
            has_r18 = self.info['has_r18']
            no_h = self.info['no_h']

            self.relate_labels = {}

            for i in illusts:
                url = i['image_urls']['square_medium']
                title = i['title']
                file_name = str(i['id'])

                #['url', 'temp_path', 'user_id', 'api']
                info = {'url': url, 'title': title, 'illust_id': file_name, 'temp_path': temp_path, 'api': api, 'illust': i, 'has_r18': has_r18, 'no_h': no_h}    # illust 是为了点击时传递给Main_Pixiv.main_pixiv.show_big_pic

                self.relate_labels[file_name] = Illust_Relate_Pic_Label(self, info=info)
                self.relate_labels[file_name].resize(124, 124)
                label_y = (math.ceil(self.pic_num / 5) - 1) * 124  + 12# (0/1/.../5) * 124, 加上12是为了让放大后的在边缘的图可以显示完全
                label_x = (self.pic_num % 5) * 124 + 12 # 加上12是为了让放大后的图可以显示完全
                self.relate_labels[file_name].move(label_x, label_y)
                self.relate_labels[file_name].set_is_loading(True)
                self.relate_labels[file_name].get_relate_pic()
                self.relate_labels[file_name].set_original_geometry(label_x, label_y, 124, 124)
                self.relate_labels[file_name].click.connect(self.label_is_clicked)
                self.relate_labels[file_name].show()
                self.pic_num += 1

    def label_is_clicked(self, info={}):
        self.one_label_is_clicked.emit(info)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QMainWindow
    from utils.Process_Token import login_info_parser
    from Pixiv_Api.My_Api import my_api
    from pixivpy3 import ByPassSniApi
    from utils.Project_Setting import setting

    cfg = login_info_parser()
    info = cfg.get_token()
    ppp = setting()
    api = my_api()
    api.hosts = api.require_appapi_hosts('public-api.secure.pixiv.net')
    api.auth(refresh_token=info['token'])

    _info = {'api': api, 'temp_path': ppp.temp_path, 'illust_id': 63639917, 'has_r18': False, 'no_h': './RES/no_h'}

    app = QApplication(sys.argv)

    m = QMainWindow()
    i = Illust_Relate(parent=m, info=_info)
    from prettyprinter import cpprint
    i.one_label_is_clicked.connect(lambda x: cpprint(x))
    i.setGeometry(QRect(0, 0, 620 + 24, 744 + 24))
    #i.setStyleSheet('background-color: rgb(154, 240, 155)')
    i.show()
    m.resize(i.width(), i.height())
    m.move(2000, 1000)
    m.show()
    sys.exit(app.exec_())