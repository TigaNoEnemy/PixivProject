#!/usr/bin/env python3
import sys
sys.path.append('.')

from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QTimer


from qtcreatorFile.commentWidget import Ui_commentWidget
from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.one_comment import One_Comment

import cgitb
cgitb.enable(format='text', logdir='log_file')
class Comment_Widget(QFrame, Ui_commentWidget):
    """info需要api, temp_path, illust"""
    #edit_comment_frame_h_diff = 210    # 编辑评论的frame动画高度差
    loading_timer_start_num = 5
    white_circle_radius = 20
    blue_circle_radius = 10

    def __init__(self, parent, info={}, *args, **kwargs):
        super(Comment_Widget, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.comment_num = 0    # 评论数
        self.info = info
        self.get_comment()

        # 下载评论列表时的动作所需的配置
        self.is_loading = True
        self.rotate = 90
        self.loading_timer = QTimer()
        self.loading_timer.timeout.connect(self.change_rotate)
        self.loading_timer.start(self.loading_timer_start_num)
        ###

    def change_rotate(self):
        self.rotate += 1.5
        
    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF
        super(Comment_Widget, self).paintEvent(qevent)

        if self.is_loading:
            width = self.comments_scroll.width()
            height = self.comments_scroll.height()
            load_x = (width - self.white_circle_radius)//2
            if height < self.height():
                load_y = height - self.white_circle_radius * 2       # comments_scroll底端往上移一个白圈直径的距离
            else:
                load_y = self.height() - (self.white_circle_radius * 2) # 最外层frame底端往上移一个白圈直径的距离
                
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, self.white_circle_radius, self.white_circle_radius)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            white_blue_diff = (self.white_circle_radius - self.blue_circle_radius) // 2
            painter.drawArc(QRectF(load_x+white_blue_diff, load_y+white_blue_diff, self.blue_circle_radius, self.blue_circle_radius), -self.rotate*16, -90*16)# 画圆环, 进度条
        else:
            if self.loading_timer.isActive():
                self.loading_timer.stop()

        self.update()

    def get_comment(self, **next_url_args):
        api = self.info['api']
        illust = self.info['illust']

        self.is_loading = True

        if not next_url_args:
            self.get_comment_thread = base_thread(self, api.illust_comments, info={}, illust_id=illust)
        else:
            next_url_args.pop('illust_id', None)
            self.get_comment_thread = base_thread(self, api.illust_comments, info={}, illust_id=illust, **next_url_args)

        self.get_comment_thread.finish.connect(self.load_comments_widget)
        self.get_comment_thread.wait()
        self.get_comment_thread.start()
        self.next_url = None

    def load_comments_widget(self, info):
        # 加载评论框架
        self.is_loading = False
        if info.get('ERROR', False):
            self.get_comment()

        else:
            comments = info['comments']
            api = self.info['api']
            temp_path = self.info['temp_path']

            try:
                self.comment_scrollArea.verticalScrollBar().valueChanged.disconnect(self.slide_down)
            except Exception as e:
                print(e)
            self.comment_scrollArea.verticalScrollBar().valueChanged.connect(self.slide_down)
            self.next_url = info['next_url']

            if comments:
                for i in comments:
                    i['api'] = api
                    i['temp_path'] = temp_path
                    p = One_Comment(self.comments_scroll, info=i)
                    p.move(0, self.comment_num * p.height())
                    self.comments_scroll.resize(self.comments_scroll.width(), (self.comment_num+1) * p.height())
                    p.show()
                    self.comment_num += 1
                if not self.next_url:
                    self.comments_scroll.resize(338, self.comments_scroll.height()+50)
                    label = QLabel(self.comments_scroll)
                    label.setObjectName('no_more_comment_label')
                    label.setText('暂无更多评论')
                    label.adjustSize()
                    x = (self.comments_scroll.width() - label.width()) // 2
                    y = self.comments_scroll.height() - 30
                    label.move(int(x), int(y))
                    label.show()

            else:
                self.comments_scroll.resize(338, 50)
                label = QLabel(self.comments_scroll)
                label.setObjectName('no_more_comment_label')
                label.setText('暂无评论')
                label.adjustSize()
                x = (self.comments_scroll.width() - label.width()) // 2
                y = self.comments_scroll.height() - 30
                label.move(int(x), int(y))
                label.show()

    def slide_down(self, new_value):
        m = self.comment_scrollArea.verticalScrollBar().maximum()
        if m - new_value <= 250 and self.next_url and not self.is_loading:
            self.comments_scroll.resize(338, self.comments_scroll.height()+50)
            self.loading_timer.start(self.loading_timer_start_num)
            next_url_args = self.info['api'].parse_qs(self.next_url)
            self.get_comment(**next_url_args)

    def resizeEvent(self, qevent):
        w = self.width()
        h = self.height()

        self.comment_scrollArea.resize(w, h)



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

    _info = {'illust': 52615680, 'api': api, 'temp_path': l_cfg.temp_path}
    #_info = {'illust': 57782374, 'api': api, 'temp_path': l_cfg.temp_path}

    app = QApplication(sys.argv)
    m = QMainWindow()
    f = open('Main_Style.qss', encoding='utf-8')
    style = f.read()
    f.close()
    m.setStyleSheet(style)
    c = Comment_Widget(m, info=_info)
    #c.setStyleSheet('#commentWidget{background-image: url(./RES/background.jpg);}')
    c.move(0, 0)
    m.resize(c.width(), c.height())
    m.show()
    print('done')
    sys.exit(app.exec_())
