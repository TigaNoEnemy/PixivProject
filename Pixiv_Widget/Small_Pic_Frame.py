#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QLabel, QPushButton
from PyQt5.QtCore import QRect, pyqtSignal, Qt, QTimer
from PyQt5.Qt import QPropertyAnimation
from PyQt5.QtGui import QPixmap
from PyQt5 import sip
import os

try:
    from Pixiv_Thread.My_Thread import base_thread
    from qtcreatorFile.small_pic_frame import Ui_small_pic_frame
except :
    import sys
    sys.path.append('.')
    from Pixiv_Thread.My_Thread import base_thread
    from qtcreatorFile.small_pic_frame import Ui_small_pic_frame

from Pixiv_Api.My_Api import my_api
from utils.Project_Setting import setting


import cgitb
cgitb.enable(format='text', logdir='log_file')
class small_pic_frame(QFrame, Ui_small_pic_frame):
    # 预览图片
    # 小图的框架
    download = pyqtSignal(dict)     # 用于通知app该作品需要创建多少个download_progress
    progress = pyqtSignal(dict)     # 用于通知app创建download_progress
    pic_click = pyqtSignal(dict)
    timeout = 3
    def __init__(self, parent, info={}):
        super(small_pic_frame, self).__init__(parent)
        self.info = info    # info共有七个键illust、start_row(创建进度条需要)、
        self.rotate = 90
        self.is_loding = True
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.change_rotate)
        self.check_info()
        self.setupUi(self)

        self.load_pic_success = False   #当图片加载不成功时，为False，不响应点击图片的动作
        self.picLabel.click.connect(self.pic_is_clicked)
        self.picLabel.info = self.info
        self.api = my_api()
        self.cfg = setting()
        self.picLabel.double_click_time = 1
        self.my_set()

    def change_rotate(self):
        self.rotate += 1

    def check_info(self):
        key = ['illust', 'start_row', 'main']

    def my_set(self):
        # 加载图片，文本
        tags = self.info['illust']['tags']
        is_bookmarked = self.info['illust']['is_bookmarked']
        illust_id = self.info['illust']['id']
        illust_title = self.info['illust']['title']
        author = self.info['illust']['user']['name']
        url = self.info['illust']['image_urls']['square_medium']

        page_count = self.info['illust']['page_count']

        if not is_bookmarked and illust_id:
            self.likeButton.setText('好き')
            self.likeButton.clicked.connect(self.add_favor)
        elif is_bookmarked and illust_id:
            self.likeButton.setText('いやです')
            self.likeButton.clicked.connect(self.del_favor)

        if not self.cfg.has_r18 and 'R-18' in str(tags):
            file = self.cfg.no_h
        elif 'R-18' in str(tags):
            file_name = f'{illust_id}_r18'
            file = f"{self.cfg.temp_path}/{file_name}"
        else:
            file_name = illust_id
            file = f"{self.cfg.temp_path}/{file_name}"

        if page_count > 1:
            self.picnNumLabel.setText(str(page_count))
        else:
            self.picnNumLabel.deleteLater()
            sip.delete(self.picnNumLabel)

        self.s_saveButton.setText('刷新')
        self.is_loding = True
        # self.timer.start(16)

        info={'file': file, 'self': 'small'}
        if not os.path.exists(file):
            self.download_small_pic_thread = base_thread(self, self.api.cache_pic, info=info, url=url, file_name=file_name, path=self.cfg.temp_path, timeout=self.timeout)
            self.download_small_pic_thread.finish.connect(self.load_complete_pic)
            self.download_small_pic_thread.wait()
            self.download_small_pic_thread.start()

        else:
            self.load_complete_pic(info=info)

        self.textLabel.setText(illust_title)
        self.authLabel.setText(f'作者：{author}')

    def add_favor(self):
        illust_id = self.info['illust']['id']
      
        self.likeButton.setEnabled(False)
        self.baseThread = base_thread(self, self.api.illust_bookmark_add, illust_id=illust_id, info={'mode': 'add'})
        self.baseThread.finish.connect(self.change_like_button)
        self.baseThread.wait()
        self.baseThread.start()

    def change_like_button(self, info):
        self.likeButton.disconnect()
        if info['mode'] == 'add':
            self.likeButton.clicked.connect(self.del_favor)
            self.likeButton.setText('いやです')
        elif info['mode'] == 'delete':
            self.likeButton.clicked.connect(self.add_favor)
            self.likeButton.setText('好き')

        self.likeButton.setEnabled(True)

    def del_favor(self):
        illust_id = self.info['illust']['id']
        
        self.likeButton.setEnabled(False)
        self.baseThread = base_thread(self, self.api.illust_bookmark_delete, illust_id=illust_id, info={'mode': 'delete'})
        self.baseThread.finish.connect(self.change_like_button)
        self.baseThread.wait()
        self.baseThread.start()

    #@profile
    def load_complete_pic(self, info):
        self.is_loding = False
        main = self.info['main']
        illust = self.info['illust']

        file = info['file']
        picture = QPixmap(file)
        if picture.isNull():
            self.s_saveButton.setText('刷新')
            self.s_saveButton.clicked.connect(self.reload)
            picture = QPixmap(self.cfg.timeout_pic)
        else:
            self.s_saveButton.setText('保存原图')
            self.s_saveButton.clicked.connect(lambda: main.saveOriginalPic(illust))
            self.load_pic_success = True

        self.picLabel.resize(234, 234)
        picture = picture.scaled(234, 234, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picLabel.setPixmap(picture)

    #@profile
    def reload(self, _):
        illust_id = self.info['illust']['id']
        url = self.info['illust']['image_urls']['square_medium']

        tags = self.info['illust']['tags']

        if 'R-18' in str(tags):
            file_name = f'{illust_id}_r18'
            file = f"{self.cfg.temp_path}/{file_name}"
        else:
            file_name = illust_id
            file = f"{self.cfg.temp_path}/{file_name}"
        try:
            os.remove(file)
        except:
            pass
        self.is_loding = True
        # self.timer.start(16)
        self.picLabel.resize(0, 0)
        self.s_saveButton.disconnect()
        self.download_small_pic_thread = base_thread(self, self.api.cache_pic, info={'file': file}, url=url, file_name=file_name, path=self.cfg.temp_path, timeout=self.timeout)
        self.download_small_pic_thread.finish.connect(self.load_complete_pic)
        self.download_small_pic_thread.wait()
        self.download_small_pic_thread.start()

    def pic_is_clicked(self, info):
        if self.load_pic_success:
            self.pic_click.emit(info)

    def remove_imperfect_image(self, file, image_size):
        # 删除不完整的图片
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            if file_size < image_size:
                try:
                    os.remove(file)
                except:
                    return False
                return True
            return False
        return True

    def start_animation(self):
        self_x = self.info['self_x']
        self_y = self.info['self_y']

        self.animation = QPropertyAnimation(self)
        self.animation.setPropertyName(b'geometry')
        self.animation.setTargetObject(self)
        self.animation.setStartValue(
            QRect(self_x+(234//2), self_y+(405//2), 0, 0))
        self.animation.setEndValue(
            QRect(self_x, self_y, 234, 405))
        self.animation.setDuration(200)
        self.animation.start()

    def paintEvent(self, qevent):
        # from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
        # from PyQt5.QtCore import QRectF

        # if self.is_loding:
        #     load_x = (234-50)//2
        #     load_y = (234-50)//2

        #     painter = QPainter(self)
        #     painter.setPen(Qt.NoPen)
        #     painter.setRenderHints(QPainter.Antialiasing)
        #     painter.setBrush(QBrush(QColor(255, 255, 255)))
        #     painter.drawEllipse(load_x, load_y, 50, 50)

        #     pen = QPen()
        #     pen.setColor(QColor("#5481FF"))
        #     pen.setWidth(3)
        #     painter.setPen(pen)
        #     painter.drawArc(QRectF(load_x, load_y, 50, 50), -self.rotate * 16, -90 * 16)
        # else:
        #     self.timer.stop()

        self.update()


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

    key = ['illust', 'start_row', 'main']
    start_row = 0
    f =['test']
    f = {j: i for i, j in enumerate(f)}
    app = QApplication(sys.argv)
    main = None
    illust = {'id': 74536659, 'title': 'Bloodborne-Doll', 'type': 'illust', 'image_urls': {'square_medium': 'https://i.pximg.net/c/540x540_10_webp/img-master/img/2019/05/05/21/06/25/74536659_p0_square1200.jpg', 'medium': 'https://i.pximg.net/c/540x540_70/img-master/img/2019/05/05/21/06/25/74536659_p0_master1200.jpg', 'large': 'https://i.pximg.net/c/600x1200_90_webp/img-master/img/2019/05/05/21/06/25/74536659_p0_master1200.jpg'}, 'caption': '', 'restrict': 0, 'user': {'id': 5435812, 'name': 'Vittorio Veneto', 'account': 'fayuuka', 'profile_image_urls': {'medium': 'https://i.pximg.net/user-profile/img/2019/03/11/22/48/45/15510276_e3b1036f8dc5a8c3364f7716991893db_170.jpg'}, 'is_followed': False}, 'tags': [{'name': 'Bloodborne', 'translated_name': None}, {'name': '人形', 'translated_name': '人偶'}, {'name': 'ブラッドボーン', 'translated_name': '血源诅咒'}], 'tools': ['SAI', 'Photoshop'], 'create_date': '2019-05-03T19:32:26+09:00', 'page_count': 2, 'width': 907, 'height': 1615, 'sanity_level': 2, 'x_restrict': 0, 'series': None, 'meta_single_page': {}, 'meta_pages': [{'image_urls': {'square_medium': 'https://i.pximg.net/c/360x360_10_webp/img-master/img/2019/05/05/21/06/25/74536659_p0_square1200.jpg', 'medium': 'https://i.pximg.net/c/540x540_70/img-master/img/2019/05/05/21/06/25/74536659_p0_master1200.jpg', 'large': 'https://i.pximg.net/c/600x1200_90_webp/img-master/img/2019/05/05/21/06/25/74536659_p0_master1200.jpg', 'original': 'https://i.pximg.net/img-original/img/2019/05/05/21/06/25/74536659_p0.jpg'}}, {'image_urls': {'square_medium': 'https://i.pximg.net/c/360x360_10_webp/img-master/img/2019/05/05/21/06/25/74536659_p1_square1200.jpg', 'medium': 'https://i.pximg.net/c/540x540_70/img-master/img/2019/05/05/21/06/25/74536659_p1_master1200.jpg', 'large': 'https://i.pximg.net/c/600x1200_90_webp/img-master/img/2019/05/05/21/06/25/74536659_p1_master1200.jpg', 'original': 'https://i.pximg.net/img-original/img/2019/05/05/21/06/25/74536659_p1.jpg'}}], 'total_view': 1151, 'total_bookmarks': 100, 'is_bookmarked': False, 'visible': True, 'is_muted': False}  
    f = {'illust': illust, 'main': main, 'start_row': start_row}
    a = small_pic_frame(parent=None, info=f)
    # a.textLabel.setText('Test')
    # a.authLabel.setText('Test')

    a.show()
    sys.exit(app.exec_())