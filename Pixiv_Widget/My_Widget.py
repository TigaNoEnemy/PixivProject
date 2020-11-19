#!/usr/bin/env python3
from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import sip

import os 
import sys
sys.path.append('.')
from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.My_Label import Largable_Label
from Pixiv_Widget.My_Label import Loading_Label
from Pixiv_Widget.Clickable_Label import clickable_label

import cgitb
cgitb.enable(format='text', logdir='log_file')
class my_widget(QWidget):
    def __init__(self, parent=None, flag=''):
        super(my_widget, self).__init__(parent)
        self.flag = flag
        self.is_loading = True
        self.rotate = 90
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_rotate)
        self.timer.start(5)

        self.load_time = 1 # 请求次数

    def change_rotate(self):
        self.rotate += 1

    def set_loading(self, p):
        self.is_loading = p

    def add_load_time(self, value):
        self.load_time += value

    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF, Qt, QPointF

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = (width-50)//2
            load_y = (height-50)//2

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, 50, 50)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x, load_y, 50, 50), -self.rotate*16, -90*16)# 画圆环, 进度条

            font = QFont('MicroSoft YaHei', 17, QFont.Bold, False)
            painter.setFont(font)
            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            painter.setPen(pen)
            font_width = painter.fontMetrics().width(str(self.load_time))
            font_height = painter.fontMetrics().height()
            painter.drawText(QPointF((width-font_width)//2+1, (height-font_height)//2+font_height/1.3), str(self.load_time))

        else:
            self.timer.stop()

        self.update()

    def close(self):
        super(my_widget, self).close()

class Scroll_Widget(QWidget):
    """调整大图位置"""
    def adjust_size(self):
        height = 0
        width = self.width()
        for i in self.children():
            children_x = (width - i.width()) // 2
            i.move(children_x, height)
            if i.height() <= 10:
                child_h = 611
            else:
                child_h = i.height()
            height += child_h
            height += 5

        self.resize(self.width(), height)

class Show_Head_Label(QLabel):
    def __init__(self, parent=None, info={}, *args, **kwargs):
        super(Show_Head_Label, self).__init__(parent)
        self.info = info
        self.is_loading = True
        self.rotate = 90
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_rotate)
        self.timer.start(5)
        self.setPixmap(QPixmap(''))

    # def check_info(self):
    #     key = ['url', 'temp_path', 'user_id', 'api']
    #     need_key = []
    #     need_not_key = []
    #     for i in self.info:
    #         if i not in key:
    #             need_not_key.append(i)
    #     for i in key:
    #         if i not in self.info:
    #             need_key.append(i)
    #     if (need_key or need_not_key) and 'test' not in self.info:
    #         print(self.info)
    #         raise KeyError(f"{str(self)} doesn't need {need_not_key} and need {need_key}")

    def set_is_loading(self, value):
        self.setPixmap(QPixmap(""))
        self.is_loading = value
        if value and not self.timer.isActive():
            self.timer.start(5)

    def change_rotate(self):
        self.rotate += 1

    def get_head(self):
        url = self.info['url']
        temp_path = self.info['temp_path']
        api = self.info['api']
        file_name = f"user_{self.info['user_id']}_pic"

        file = f"{temp_path}/{file_name}"
        if os.path.exists(file):
            self.load_head({'file_name': file_name})

        else:
            self.get_head_thread = base_thread(self, api.cache_pic, url=url, path=temp_path, file_name=file_name, info={'file_name': file_name})
            self.get_head_thread.finish.connect(self.load_head)
            self.get_head_thread.wait()
            self.get_head_thread.start()

    def load_head(self, info):
        if info.get('ERROR', False):
            self.get_head()
            return
        url = self.info['url']
        temp_path = self.info['temp_path']
        api = self.info['api']

        file_name = info['file_name']

        file = f"{temp_path}/{file_name}"
        self.picture = QPixmap(file)
        if self.picture.isNull():
            try:
                os.remove(file)
            except Exception as e:
                print(e)

            self.get_head()
        else:
            self.picture = self.picture.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(self.picture)
            self.is_loading = False

    def paintEvent(self,qevent):
        from PyQt5.QtGui import QPainter, QPen, QColor, QFont,QBrush
        from PyQt5.QtCore import QRectF, Qt
        super(Show_Head_Label, self).paintEvent(qevent)

        if self.is_loading:
            width = self.width()
            height = self.height()
            load_x = width/2//2
            load_y = height/2//2

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, width-width/2, height-height/2)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x, load_y, width-width/2, height-height/2), -self.rotate*16, -90*16)# 画圆环, 进度条
        else:
            if self.timer.isActive():
                self.timer.stop()

        self.update()

class Illust_Relate_Pic_Label(Largable_Label, Show_Head_Label):
    click = pyqtSignal(dict)
    def get_relate_pic(self):
        url = self.info['url']
        temp_path = self.info['temp_path']
        api = self.info['api']
        file_name = self.info['illust_id']
        no_h = self.info['no_h']
        has_r18 = self.info['has_r18']
        tags = self.info['illust']

        if not has_r18 and 'R-18' in str(tags):
            self.file = file = no_h
        elif 'R-18' in str(tags):
            file_name = f'{file_name}_r18'
            self.file = file = f"{temp_path}/{file_name}"
        else:
            self.file = file = f"{temp_path}/{file_name}"
        if os.path.exists(file):
            self.load_relate_pic({'file': file})

        else:
            self.get_head_thread = base_thread(self, api.cache_pic, url=url, path=temp_path, file_name=file_name, info={'file': file})
            self.get_head_thread.finish.connect(self.load_relate_pic)
            self.get_head_thread.wait()
            self.get_head_thread.start()

    def load_relate_pic(self, info):
        if info.get('ERROR', False):
            try:
                os.remove(file)
            except:
                pass
            self.get_relate_pic()
            return

        file = info['file']
        self.picture = QPixmap(file)
        if self.picture.isNull():
            try:
                os.remove(file)
            except:
                pass
            self.get_relate_pic()
        else:
            self.picture = self.picture.scaled(self.width(), self.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.setPixmap(self.picture)
            self.is_loading = False

            #self.set_original_geometry(self.x(), self.y(), self.width(), self.height())

    def mouseReleaseEvent(self, qevent):
        if qevent.button() == 1 and not self.is_loading:
            self.click.emit(self.info)

class Show_User_Illust_Label(Illust_Relate_Pic_Label):
    """为搜索作者时显示的作品图片而做"""
    pass
        
        
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from utils.Process_Token import login_info_parser
    from Pixiv_Api.My_Api import my_api

    def test_show_head_label():
        cfg = login_info_parser()
        info = cfg.get_token()
        # api = my_api()

        # api.require_appapi_hosts('public-api.secure.pixiv.net')

        # api.auth(refresh_token=info['token'])

        app = QApplication(sys.argv)
        key = {'url': '', 'api': ',', 'user_id': '1652353', 'temp_path': '.'}
        a = Show_Head_Label(info=key)
        a.resize(100, 100)
        a.get_head()
        
        # b = QPixmap(f"./user_1652353_pic")
        # a.setPixmap(b)
        # a.is_loading = False
        a.show()
        sys.exit(app.exec_())

    def test_my_widget():
        app = QApplication(sys.argv)
        m = my_widget()
        m.show()
        sys.exit(app.exec_())

    test_my_widget()