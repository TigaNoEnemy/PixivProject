#!/usr/bin/env python3
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QTimer

from memory_profiler import profile

# 导入自定义模块
try:
    from Pixiv_Widget.Clickable_Label import clickable_label
    from Pixiv_Thread.My_Thread import base_thread
except:
    import sys
    sys.path.append('.')
    from Pixiv_Widget.Clickable_Label import clickable_label
    from Pixiv_Thread.My_Thread import base_thread

import cgitb

cgitb.enable(format='text', logdir='log_file')


class big_pic_frame(QFrame):
    double_click = pyqtSignal(dict)   # 双击显示原图
    # click = pyqtSignal()          # 单击重载图片
    # timer = QTimer()

    def __init__(self, parent, info):
        super(big_pic_frame, self).__init__(parent)
        self.info = info
        self.check_info()
        self.change_file_name()
        self.pic_size = 1
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
        key = ['api', 'url', 'temp_path', 'temp_file_name', 'title', 'timeout_pic', 'original_pic_url', 'tags', 'illust_id']
        need_key = []
        need_not_key = []
        for i in self.info:
            if i not in key:
                need_not_key.append(i)
        for i in key:
            if i not in self.info:
                need_key.append(i)
        if need_key or need_not_key:
            raise KeyError(f"big_pic_frame doesn't need {need_not_key} and need {need_key}")

    def setupUi(self):
        url = self.info['url']
        temp_path = self.info['temp_path']
        temp_file_name = self.info['temp_file_name']
        title = self.info['title']
        timeout_pic = self.info['timeout_pic']

        self.bigPicLabel = clickable_label(self, self.info)
        self.bigPicLabel.setGeometry(QRect(0, 0, 620, 611))
        self.bigPicLabel.setObjectName("bigPicLabel")
        self.bigPicLabel.setObjectName("picLabel")
     
        self.bigPicLabel.setAlignment(Qt.AlignCenter)

        info = {'temp_file_name': temp_file_name, 'url': url, 'temp_path': temp_path, 'title': title, 'timeout_pic': timeout_pic, 'self': 'big'}

        self.create_get_pic_size_thread(info)

    def create_get_pic_size_thread(self, info, is_reload=False):
        import os

        api = self.info['api']
        
        temp_path = info['temp_path']
        temp_file_name = info['temp_file_name']
        url = info['url']
        if is_reload:
            try:
                os.remove(f"{temp_path}/{temp_file_name}")
            except:
                pass
        self.is_loading  = True
        self.picture = QPixmap('')
        self.bigPicLabel.setPixmap(self.picture)
        if os.path.exists(f"{temp_path}/{temp_file_name}"):
            print('Big file is exists.')
            info['isSuccess'] = True
            self.load_big_pic_complete(info)

        else:
            self.thread = base_thread(self, method=api.get_image_size, url=url, info=info)
            self.thread.finish.connect(self.create_download_thread)
            self.thread.wait()
            self.thread.start()

    def create_download_thread(self, info):

        if hasattr(self, 'thread'):
            del self.thread
        api = self.info['api']

        if not info['isSuccess']:
            self.load_big_pic_complete(info=info)
            return
        url = info['url']
        temp_path = info['temp_path']
        temp_file_name = info['temp_file_name']

        if 'image_size' in info:
            self.pic_size = info['image_size']

        self.thread = base_thread(self, method=api.cache_pic, url=url, file_name=temp_file_name, path=temp_path, info=info)
        self.thread.finish.connect(self.load_big_pic_complete)
        self.thread.wait()
        self.thread.start()

        try:
            self.bigPicLabel.disconnect()
        except:
            pass

        self.bigPicLabel.setPixmap(QPixmap(''))

    def load_big_pic_complete(self, info):
        import os

        temp_path = self.info['temp_path']
        temp_file_name = self.info['temp_file_name']
        timeout_pic = self.info['timeout_pic']
        isSuccess = info['isSuccess']

        self.is_loading = False
        try:
            self.thread.disconnect()
        except:
            pass

        if isSuccess:
            temp_file = f"{temp_path}/{temp_file_name}"
        else:
            temp_file = timeout_pic
            try:
                os.remove(f"{temp_path}/{temp_file_name}")
            except:
                pass



        self.picture = QPixmap(temp_file)

        if self.picture.isNull() or temp_file == timeout_pic:
            self.picture = QPixmap(timeout_pic)
            self.bigPicLabel.click.connect(lambda x: self.create_get_pic_size_thread(x, is_reload=True))

        self.picture = self.picture.scaled(self.bigPicLabel.width(), self.bigPicLabel.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        picture_h = self.picture.height()
        picture_w = self.picture.width()
        picture_x = int((620-picture_w)/2)

        self.bigPicLabel.setPixmap(self.picture)
        self.bigPicLabel.setGeometry(QRect(picture_x, 0, picture_w, picture_h))
        self.bigPicLabel.double_click.connect(self.pic_label_is_double_clicked)
        self.bigPicLabel.show()

    def pic_label_is_double_clicked(self):
        temp_file_name = f"{self.info['temp_file_name']}_original"

        info = self.info.copy()
        info.update({'temp_file_name': temp_file_name})
        self.double_click.emit(info)

    def paintEvent(self, qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF
        import os

        temp_path = self.info['temp_path']
        temp_file_name = self.info['temp_file_name']

        temp_file = f"{temp_path}/{temp_file_name}"
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

    key = ['api', 'url', 'temp_path', 'temp_file_name', 'title', 'timeout_pic', 'original_pic_url', 'tags', 'illust_id']
    _info = {}
    cfg = login_info_parser()
    info = cfg.get_token()
    api = my_api()
    print('翻墙')
    api.hosts = api.require_appapi_hosts('public-api.secure.pixiv.net')
    print('翻墙成功')
    print('登录')
    api.auth(refresh_token=info['token'])
    print('登陆成功')
    _info['api'] = api
    _info['url'] = 'https://i.pximg.net/c/600x1200_90_webp/img-master/img/2017/07/01/00/00/23/63639917_p4_master1200.jpg'
    _info['temp_path'] = 'pixivTmp'
    _info['temp_file_name'] = 'test'
    _info['title'] = 'test'
    _info['timeout_pic'] = 'RES/TIMEOUT.png'
    _info['original_pic_url'] = ''
    _info['tags'] = ''
    _info['illust_id'] = '63639917'
    app = QApplication(sys.argv)
    a = big_pic_frame(parent=None, info=_info)
    a.show()
    sys.exit(app.exec_())