#!/usr/bin/env python3
import sys
sys.path.append('.')

from PyQt5.QtWidgets import QFrame, QLabel

from qtcreatorFile.commentWidget import Ui_commentWidget
from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.one_comment import One_Comment


class Comment_Widget(QFrame, Ui_commentWidget):
    """info需要api, temp_path, illust"""
    edit_comment_frame_h_diff = 210    # 编辑评论的frame动画高度差

    def __init__(self, parent, info={}, *args, **kwargs):
        super(Comment_Widget, self).__init__(parent, *args, **kwargs)
        self.setupUi(self)
        self.comment_num = 0    # 评论数
        self.info = info
        self.get_comment()

    def get_comment(self, **next_url_args):
        api = self.info['api']
        illust = self.info['illust']

        if not next_url_args:
            get_comment_thread = base_thread(self, api.illust_comments, info={}, illust_id=illust)
        else:
            next_url_args.pop('illust_id', None)
            get_comment_thread = base_thread(self, api.illust_comments, info={}, illust_id=illust, **next_url_args)

        get_comment_thread.finish.connect(self.load_comments_widget)
        get_comment_thread.wait()
        get_comment_thread.start()
        self.next_url = None

    def load_comments_widget(self, info):
        # 加载评论框架
        comments = info['comments']
        api = self.info['api']
        temp_path = self.info['temp_path']

        if comments:
            for i in comments:
                i['api'] = api
                i['temp_path'] = temp_path
                p = One_Comment(self.comments_scroll, info=i)
                p.move(0, self.comment_num * p.height())
                self.comments_scroll.resize(self.comments_scroll.width(), (self.comment_num+1) * p.height())
                p.show()
                self.comment_num += 1

        else:
            self.comments_scroll.resize(338, 200)
            label = QLabel(self.comments_scroll)
            label.setText('暂无评论')
            label.adjustSize()
            x = (self.comments_scroll.width() - label.width()) // 2
            y = (self.comments_scroll.height() - label.height()) // 2
            label.move(int(x), int(y))
            label.setStyleSheet('color: rgb(255, 255, 255)')
            label.show()

        self.comment_scrollArea.verticalScrollBar().valueChanged.connect(self.slide_down)
        self.next_url = info['next_url']

    def slide_down(self, new_value):
        m = self.comment_scrollArea.verticalScrollBar().maximum()
        if m - new_value <= 250 and self.next_url:
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

    _info = {'illust': 18423302, 'api': api, 'temp_path': l_cfg.temp_path}

    app = QApplication(sys.argv)
    m = QMainWindow()
    c = Comment_Widget(m, info=_info)
    c.move(0, 0)
    m.resize(c.width(), c.height())
    m.show()
    print('done')
    sys.exit(app.exec_())
