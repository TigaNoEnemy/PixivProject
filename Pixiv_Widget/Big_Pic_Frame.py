#!/usr/bin/env python3
from PyQt5.QtWidgets import QFrame, QMenu
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QTimer

import os


# 导入自定义模块
try:
    from Pixiv_Widget.Clickable_Label import clickable_label, Big_Pic_Clickable_Label
    from Pixiv_Thread.My_Thread import base_thread
except:
    import sys
    sys.path.append('.')
    from Pixiv_Widget.Clickable_Label import clickable_label
    from Pixiv_Thread.My_Thread import base_thread

from Pixiv_Api.My_Api import my_api
from utils.Project_Setting import setting

import cgitb

cgitb.enable(format='text', logdir='log_file')

FILE = '\033[34mBig_Pic_File\033[0m'

class big_pic_frame(QFrame):
    double_click = pyqtSignal(dict)   # 双击显示原图
    click = pyqtSignal(dict)
    image_load_completly = pyqtSignal()
    download_single_pic_signal = pyqtSignal(dict)   # 下载单张图片的信号

    def __init__(self, parent, info):
        super(big_pic_frame, self).__init__(parent)
        self.info = info
        self.api = my_api()
        self.cfg = setting()
        self.check_info()
        self.change_file_name()
        self.pic_size = -1
        self.rotate = 90
        self.setupUi()
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_rotate)

    def change_file_name(self):
        tags = self.info['tags']
        temp_file_name = self.info['temp_file_name']
        if 'R-18' in str(tags):
            self.info['temp_file_name'] = f"{temp_file_name}_r18"

    def change_rotate(self):
        self.rotate += 1

    #@profile
    def check_info(self):
        # illust_id 用于检测当前显示的作品
        key = ['url', 'temp_file_name', 'title', 'original_pic_url', 'tags', 'illust_id', 'pic_no']

    def setupUi(self):
        url = self.info['url']
        temp_file_name = self.info['temp_file_name']
        title = self.info['title']

        self.bigPicLabel = Big_Pic_Clickable_Label(self, self.info)
        self.bigPicLabel.setGeometry(QRect(0, 0, 620, 611))
        # self.bigPicLabel.setObjectName("bigPicLabel")
        self.bigPicLabel.setObjectName("picLabel")
        self.bigPicLabel.setAlignment(Qt.AlignCenter)
        self.bigPicLabel.right_click.connect(self.show_action)

        info = {'temp_file_name': temp_file_name, 'url': url, 'temp_path': self.cfg.temp_path, 'title': title, 'timeout_pic': self.cfg.timeout_pic, 'self': 'big'}

        self.create_get_pic_size_thread(info)

    def show_action(self, info):
        self.qmenu = QMenu()
        force_reload = self.qmenu.addAction('强制重载')
        download_pic = self.qmenu.addAction('保存原图')

        if self.is_loading:
            force_reload.setEnabled(False)
            download_pic.setEnabled(False)
        elif self.picture.isNull():
            force_reload.triggered.connect(lambda x: self.force_reload(info))
            download_pic.setEnabled(False)
        else:
            force_reload.triggered.connect(lambda x: self.force_reload(info))
            download_pic.triggered.connect(lambda x: self.download_single_pic(info))

        self.qmenu.exec(QCursor.pos())

    def force_reload(self, info):
        temp_file_name = info['temp_file_name']
        file = f"{self.cfg.temp_path}/{temp_file_name}"
        try:
            os.remove(file)
        except Exception as e:
            print(f"{FILE}: {e}")
        self.create_get_pic_size_thread(info, is_reload=True)

    def download_single_pic(self, info):
        # 伪造只有一张图片的作品
        illust = {}
        illust['title'] = info['title']
        illust['id'] = info['illust_id']
        illust['meta_single_page'] = {}
        illust['meta_single_page']['original_image_url'] = info['original_pic_url']
        illust['meta_pages'] = []
        illust['pic_no'] = info['pic_no']
        print(illust)
        ###
        self.download_single_pic_signal.emit(illust)

    def create_get_pic_size_thread(self, info, is_reload=False):
        temp_file_name = info['temp_file_name']
        url = info['url']
        if is_reload:
            try:
                self.bigPicLabel.click.disconnect()
            except Exception as e:
                print(f"{FILE}: {e}")
            # try:
            #     os.remove(f"{self.cfg.temp_path}/{temp_file_name}")
            # except Exception as e:
            #     print('='*60)
            #     print(f"{FILE}: {e}")
        self.is_loading  = True
        self.picture = QPixmap('')
        self.bigPicLabel.setPixmap(self.picture)
        file = f"{self.cfg.temp_path}/{temp_file_name}"
        try:
            had_downloaded_size = os.path.getsize(file)
        except FileNotFoundError:
            had_downloaded_size = 0
        size = f"bytes={had_downloaded_size}-"
        self.thread = base_thread(None, method=self.api.get_image_size, url=url, Range=size, info=info)
        self.thread.finish.connect(self.create_download_thread)
        self.thread.wait()
        self.thread.start()

    def create_download_thread(self, info):
        try:
            del self.thread
        except AttributeError:
            pass

        if not info['isSuccess']:
            self.load_big_pic_complete(info=info)
            return
        temp_file_name = info['temp_file_name']
        response = info['response']
        output_file = f"{self.cfg.temp_path}/{temp_file_name}"

        self.pic_size = info['image_size']

        self.thread = base_thread(None, method=self.api.download_has_size_pic, response=response, output_file=output_file)
        self.thread.finish.connect(self.load_big_pic_complete)
        self.thread.wait()
        self.thread.start()

        try:
            self.bigPicLabel.double_click.disconnect(self.pic_label_is_double_clicked)
        except Exception as e:
            print(f'{FILE}: {e}')

        self.bigPicLabel.setPixmap(QPixmap(''))

    def load_big_pic_complete(self, info):
        import os

        temp_file_name = self.info['temp_file_name']
        #isSuccess = info['isSuccess']

        self.is_loading = False
        try:
            self.thread.disconnect()
        except:
            pass
        
        temp_file = f"{self.cfg.temp_path}/{temp_file_name}"
        self.picture = QPixmap(temp_file)
        self.bigPicLabel.set_load_pic_seccess(True)
        if self.picture.isNull():
            # try:
            #     os.remove(f"{self.cfg.temp_path}/{temp_file_name}")
            # except:
            #     pass
            self.bigPicLabel.click.connect(lambda x: self.create_get_pic_size_thread(x, is_reload=True))
            self.picture = QPixmap(self.cfg.timeout_pic)
            self.bigPicLabel.set_load_pic_seccess(False)
        else:
            self.bigPicLabel.click.connect(self.click.emit)

        pic_width = self.picture.width()
        if pic_width > 620:
            pic_height = int(self.picture.height() / (pic_width / 620))
            pic_width = 620
        else:
            pic_height = self.picture.height()
        self.bigPicLabel.resize(pic_width, pic_height)
        self.resize(pic_width, pic_height)            

        self.picture = self.picture.scaled(self.bigPicLabel.width(), self.bigPicLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # picture_h = self.picture.height()
        # picture_w = self.picture.width()
        # picture_x = int((620-picture_w)/2)

        self.bigPicLabel.setPixmap(self.picture)
        #self.bigPicLabel.setGeometry(QRect(picture_x, 0, picture_w, picture_h))
        self.bigPicLabel.double_click.connect(self.pic_label_is_double_clicked)
        self.bigPicLabel.show()

        self.image_load_completly.emit()

    def pic_label_is_double_clicked(self):
        temp_file_name = f"{self.info['temp_file_name']}_original"

        info = self.info.copy()
        info.update({'temp_file_name': temp_file_name})
        self.double_click.emit(info)

    def paintEvent(self, qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF
        import os

        temp_file_name = self.info['temp_file_name']

        temp_file = f"{self.cfg.temp_path}/{temp_file_name}"
        try:
            file_size = os.path.getsize(temp_file)
        except FileNotFoundError:
            file_size = 0

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = (width-50)//2
            load_y = (height-50)//2

            percent = file_size/self.pic_size
            rotateAngle = 360*percent
            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, 50, 50)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            if self.pic_size == -1:
                if not self.timer.isActive():
                    self.timer.start(10)
                painter.drawArc(QRectF(load_x, load_y, 50, 50), -self.rotate*16, -90*16)
            else:
                painter.drawArc(QRectF(load_x, load_y, 50, 50), 90*16, -rotateAngle*16)#(0 - 0) * 0, -rotateAngle * 16)  # 画圆环, 进度条
                font = QFont()
                font.setFamily("微软雅黑")
                font.setPointSize(11)
                painter.setFont(font)
                painter.setPen(QColor("#5481FF"))
                painter.drawText(QRectF(load_x, load_y, 50, 50), Qt.AlignCenter, f"{int(percent*100)}%")  # 显示进度条当前进度
        else:
            if self.timer.isActive():
                self.timer.stop()

        self.update()

if __name__ == '__main__':
    from utils.Process_Token import login_info_parser
    from Pixiv_Api.My_Api import my_api
    from PyQt5.QtWidgets import QApplication
    import sys

    
    key = ['url', 'temp_path', 'temp_file_name', 'title', 'timeout_pic', 'original_pic_url', 'tags', 'illust_id']
    _info = {}
    cfg = login_info_parser()
    info = cfg.get_token()
    proxies = {
        'http': '127.0.0.1:8888',
        'https': '127.0.0.1:8888',
    }
    api = my_api()
    print('翻墙')
    api.pximg = api.require_appapi_hosts("i.pximg.net")
    api.hosts = api.require_appapi_hosts("public-api.secure.pixiv.net")
    api.default_head = api.require_appapi_hosts("s.pximg.net")
    print('翻墙成功')
    print('登录')
    api.auth(refresh_token=info['token'])
    print('登陆成功')
    _info['api'] = api
    _info['url'] = 'https://210.140.92.140/c/600x1200_90_webp/img-master/img/2019/04/06/15/37/40/74069608_p1_master1200.jpg'
    _info['temp_path'] = 'pixivTmp'
    _info['temp_file_name'] = 'test'
    _info['title'] = 'test'
    _info['timeout_pic'] = 'RES/TIMEOUT.png'
    _info['original_pic_url'] = 'I\'m original_pic_url'
    _info['tags'] = ''
    _info['illust_id'] = '85213770'
    app = QApplication(sys.argv)
    a = big_pic_frame(parent=None, info=_info)
    # a.move(2000, 1000)
    # a.resize(100, 50)
    # a.setMaximumSize(100, 50)
    a.show()
    sys.exit(app.exec_())