#!/usr/bin/env python3

from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import QRect, pyqtSignal, Qt, QRectF, QTimer
from PyQt5.QtGui import QMovie, QPixmap, QPainter, QPen, QFont, QColor, QBrush
import os
import sys
sys.path.append('.')

from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.Clickable_Label import clickable_label
from Pixiv_Api.My_Api import my_api
from utils.Project_Setting import setting



import cgitb
cgitb.enable(format='text', logdir='log_file')
class original_pic(QMainWindow):
    # 显示原图
    myclosed = pyqtSignal(dict)
    timeout = 10

    def __init__(self, parent=None, info={}):
        super(original_pic, self).__init__()
        self.info = info
        self.cfg = setting()
        self.api = my_api()
        self._parent = parent
        self.is_loading = True
        self.original_pic_size = -1
        self.rotate = 90
        self.timer = QTimer()
        self.timer.timeout.connect(self.add_rotate)
        self.check_info()
        self.setupUi()
        #self.setStyleSheet('background-color: rgb(230, 230, 230)')
        self.move_self_to_center()

    def add_rotate(self):
        self.rotate += 1

    def move_self_to_center(self):
        parent_x = self._parent.x()
        parent_y = self._parent.y()
        parent_w = self._parent.width()
        parent_h = self._parent.height()
        width = self.width()
        height = self.height()

        x = (parent_w - width) // 2
        y = (parent_h - height) // 2
        self.move(x + parent_x, y + parent_y)

    def check_info(self):
        key = ['url', 'temp_file_name', 'title', 'timeout_pic']

    def setupUi(self):
        title = self.info['title']

        self.setWindowTitle(title)

        self.sub_label = clickable_label(self)
        self.sub_label.setGeometry(QRect(0,0,0,0))

        self.sub_label.setAlignment(Qt.AlignCenter)
        self.show()
        self.resize(800, 600)
        self.create_get_img_size_thread()

    def create_get_img_size_thread(self):
        url = self.info['url']
        temp_file_name = self.info['temp_file_name']

        file = f"{self.cfg.temp_path}/{temp_file_name}"
        self.is_loading = True
        self.sub_label.resize(0, 0)
        try:
            self.sub_label.disconnect()
        except:
            pass

        self.sub_label.setPixmap(QPixmap(''))

        try:
            had_pic_size = os.path.getsize(file)
        except FileNotFoundError:
            had_pic_size = 0

        Range = f"bytes={had_pic_size}-"
        
        print(file)
        info = {'file': file, 'url': url}
        # if not os.path.exists(file):
        self.get_img_size_thread = base_thread(self, self.api.get_image_size, info=info, url=url, timeout=self.timeout, Range=Range)
        self.get_img_size_thread.finish.connect(self.create_download_thread)
        self.get_img_size_thread.wait()
        self.get_img_size_thread.start()
        # else:
        #     info['isSuccess'] = True
        #     self.load_original_pic(info)

    def create_download_thread(self, info):
        if not info['isSuccess']:
            self.create_get_img_size_thread()
            return

        url = self.info['url']
        temp_file_name = self.info['temp_file_name']

        file = f"{self.cfg.temp_path}/{temp_file_name}"

        response = info['response']

        self.original_pic_size = info['image_size']

        self.show_original_threads = base_thread(self, self.api.download_has_size_pic, response=response, output_file=file)
        self.show_original_threads.finish.connect(self.load_original_pic)
        self.show_original_threads.start()

    def load_original_pic(self, info):
        is_success = info['isSuccess']
        temp_file_name = self.info['temp_file_name']

        temp_file = f"{self.cfg.temp_path}/{temp_file_name}"
        self.is_loading = False
        if is_success:
            file = temp_file
        else:
            file = self.cfg.timeout_pic
        
        self.picture = QPixmap(file)
        # temp_file_size = os.path.getsize(temp_file)
        # if self.picture.isNull() or file == self.cfg.timeout_pic or temp_file_size < self.original_pic_size:
        #     self.sub_label.double_click.connect(self.create_get_img_size_thread)
        #     try:
        #         os.remove(temp_file)
        #     except Exception as e:
        #         print(e)
        self.sub_label.double_click.connect(self.create_get_img_size_thread)
        width = self.width()
        height = self.height()
        sub_label_w, sub_label_h = self.ajust_label_size(width, height)

        picture = self.picture.scaled(sub_label_w, sub_label_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        try:
            self.sub_label.setPixmap(picture)
        except KeyError as e:
            print(e)
        else:
            sub_label_x = (width - sub_label_w)//2
            sub_label_y = (height - sub_label_h)//2
            self.sub_label.setGeometry(QRect(sub_label_x, sub_label_y, sub_label_w, sub_label_h))
        if self.timer.isActive():
            self.timer.stop()

    def resizeEvent(self, qevent):
        if not self.is_loading:
            width = self.width()
            height = self.height()
            sub_label_w, sub_label_h = self.ajust_label_size(width, height)

            picture = self.picture.scaled(sub_label_w, sub_label_h, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.sub_label.setPixmap(picture)
            sub_label_x = (width - sub_label_w)//2
            sub_label_y = (height - sub_label_h)//2
            self.sub_label.setGeometry(QRect(sub_label_x, sub_label_y, sub_label_w, sub_label_h))

    def paintEvent(self, qevent):
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

            percent = file_size/self.original_pic_size
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
            if self.original_pic_size == -1:
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

        self.update()


    def ajust_label_size(self, width, height) :
        picture_w = self.picture.width()
        picture_h = self.picture.height()
        if picture_w >= width:
            sub_label_w = width
        else:
            sub_label_w = picture_w

        if picture_h >= height:
            sub_label_h = height
        else:
            sub_label_h = picture_h
        return (sub_label_w, sub_label_h)


    def closeEvent(self, qevent):
        self.myclosed.emit(self.info)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtWidgets import QDesktopWidget
    app = QApplication(sys.argv)
    print('翻墙')

    api = my_api()
    api.pximg = api.require_appapi_hosts("i.pximg.net")
    api.hosts = api.require_appapi_hosts("public-api.secure.pixiv.net")
    api.default_head = api.require_appapi_hosts("s.pximg.net")
    print('翻墙成功')
    print('登录')

    info = {
            'url': 'https://210.140.92.142/img-original/img/2021/02/23/00/00/00/87977770_p0.png',
            'temp_path': './Pixiv',
            'temp_file_name': 'test',
            'api': api,
            'loading_gif': '',
            'title': 'お好みの彼女をどうぞ',
            'timeout_pic': './RES/TIMEOUT.png',
        }

    b = QDesktopWidget()
    a = original_pic(info=info, parent=b)
    a.show()

    sys.exit(app.exec_())