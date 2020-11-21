#!/usr/bin/env python3

from PyQt5.QtWidgets import QFrame, QLabel, QPushButton
from PyQt5.QtCore import QRect, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5 import sip
import os
from memory_profiler import profile

try:
    from Pixiv_Thread.My_Thread import base_thread
    from qtcreatorFile.small_pic_frame import Ui_small_pic_frame
except :
    import sys
    sys.path.append('.')
    from Pixiv_Thread.My_Thread import base_thread
    from qtcreatorFile.small_pic_frame import Ui_small_pic_frame


import cgitb
cgitb.enable(format='text', logdir='log_file')
class small_pic_frame(QFrame, Ui_small_pic_frame):
    # 预览图片
    # 小图的框架
    download = pyqtSignal(dict)     # 用于通知app该作品需要创建多少个download_progress
    progress = pyqtSignal(dict)     # 用于通知app创建download_progress
    pic_click = pyqtSignal(dict)
    timeout = 3
    def __init__(self, parent, info={}, test=False):
        super(small_pic_frame, self).__init__(parent)
        self.info = info    # info共有七个键illust、api、loading_gif(加载时的动画)、timeout_pic(加载失败时显示的图片)、temp_path(图片缓存文件夹)、start_row(创建进度条需要)、save_path(下载文件夹)
        self.rotate = 90
        self.is_loding = True
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_rotate)
        self.check_info()
        self.setupUi(self)

        self.load_pic_success = False   #当图片加载不成功时，为False，不响应点击图片的动作
        self.picLabel.click.connect(self.pic_is_clicked)
        self.picLabel.info = self.info
        self.picLabel.double_click_time = 1
        if not test:
            self.my_set()
        else:
            self.timer.start(10)

    def change_rotate(self):
        self.rotate += 1

    def check_info(self):
        key = ['illust', 'api', 'timeout_pic', 'temp_path', 'start_row', 'save_path', 'has_r18', 'no_h', 'main']
        need_key = []
        need_not_key = []
        for i in self.info:
            if i not in key:
                need_not_key.append(i)
        for i in key:
            if i not in self.info:
                need_key.append(i)
        if (need_key or need_not_key) and 'test' not in self.info:
            raise KeyError(f"small_pic_frame doesn't need {need_not_key} and need {need_key}")

    def my_set(self):
        # 加载图片，文本
        tags = self.info['illust']['tags']
        is_bookmarked = self.info['illust']['is_bookmarked']
        illust_id = self.info['illust']['id']
        illust_title = self.info['illust']['title']
        author = self.info['illust']['user']['name']
        api = self.info['api']
        url = self.info['illust']['image_urls']['square_medium']
        temp_path = self.info['temp_path']
        has_r18 = self.info['has_r18']
        no_h = self.info['no_h']

        page_count = self.info['illust']['page_count']

        if not is_bookmarked and illust_id:
            self.likeButton.setText('好き')
            self.likeButton.clicked.connect(self.add_favor)
        elif is_bookmarked and illust_id:
            self.likeButton.setText('いやです')
            self.likeButton.clicked.connect(self.del_favor)

        if not has_r18 and 'R-18' in str(tags):
            file = no_h
        elif 'R-18' in str(tags):
            file_name = f'{illust_id}_r18'
            file = f"{temp_path}/{file_name}"
        else:
            file_name = illust_id
            file = f"{temp_path}/{file_name}"

        if page_count > 1:
            self.picnNumLabel.setText(str(page_count))
        else:
            self.picnNumLabel.deleteLater()
            sip.delete(self.picnNumLabel)

        self.s_saveButton.setText('刷新')
        self.is_loding = True
        self.timer.start(16)

        info={'file': file, 'self': 'small'}
        if not os.path.exists(file):
            self.download_small_pic_thread = base_thread(self, api.cache_pic, info=info, url=url, file_name=file_name, path=temp_path, timeout=self.timeout)
            self.download_small_pic_thread.finish.connect(self.load_complete_pic)
            self.download_small_pic_thread.wait()
            self.download_small_pic_thread.start()

        else:
            self.load_complete_pic(info=info)

        self.textLabel.setText(illust_title)
        self.authLabel.setText(f'作者：{author}')

    def add_favor(self):
        illust_id = self.info['illust']['id']
        api = self.info['api']

        self.likeButton.setText('いやです')
        self.likeButton.setEnabled(False)
        self.baseThread = base_thread(self, api.illust_bookmark_add, illust_id=illust_id, info={'mode': 'add'})
        self.baseThread.finish.connect(self.change_like_button)
        self.baseThread.wait()
        self.baseThread.start()

    def change_like_button(self, info):
        self.likeButton.disconnect()
        if info['mode'] == 'add':
            self.likeButton.clicked.connect(self.del_favor)
        elif info['mode'] == 'delete':
            self.likeButton.clicked.connect(self.add_favor)

        self.likeButton.setEnabled(True)

    def del_favor(self):
        illust_id = self.info['illust']['id']
        api = self.info['api']

        self.likeButton.setText('好き')
        self.likeButton.setEnabled(False)
        self.baseThread = base_thread(self, api.illust_bookmark_delete, illust_id=illust_id, info={'mode': 'delete'})
        self.baseThread.finish.connect(self.change_like_button)
        self.baseThread.wait()
        self.baseThread.start()

    #@profile
    def load_complete_pic(self, info):
        self.is_loding = False
        timeout_pic = self.info['timeout_pic']
        main = self.info['main']
        illust = self.info['illust']

        file = info['file']
        picture = QPixmap(file)
        if picture.isNull():
            self.s_saveButton.setText('刷新')
            self.s_saveButton.clicked.connect(self.reload)
            picture = QPixmap(timeout_pic)
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
        temp_path = self.info['temp_path']
        api = self.info['api']
        url = self.info['illust']['image_urls']['square_medium']

        tags = self.info['illust']['tags']

        if 'R-18' in str(tags):
            file_name = f'{illust_id}_r18'
            file = f"{temp_path}/{file_name}"
        else:
            file_name = illust_id
            file = f"{temp_path}/{file_name}"
        try:
            os.remove(file)
        except:
            pass
        self.is_loding = True
        self.timer.start(16)
        self.picLabel.resize(0, 0)
        self.s_saveButton.disconnect()
        self.download_small_pic_thread = base_thread(self, api.cache_pic, info={'file': file}, url=url, file_name=file_name, path=temp_path, timeout=self.timeout)
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

    def paintEvent(self, qevent):
        from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
        from PyQt5.QtCore import QRectF

        if self.is_loding:
            load_x = (234-50)//2
            load_y = (234-50)//2

            painter = QPainter(self)
            painter.setPen(Qt.NoPen)
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(load_x, load_y, 50, 50)

            pen = QPen()
            pen.setColor(QColor("#5481FF"))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawArc(QRectF(load_x, load_y, 50, 50), -self.rotate * 16, -90 * 16)
        else:
            self.timer.stop()

        self.update()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

    f =['test']
    f = {j: i for i, j in enumerate(f)}
    app = QApplication(sys.argv)
    a = small_pic_frame(parent=None, info=f, test=True)
    a.textLabel.setText('Test')
    a.authLabel.setText('Test')

    a.show()
    sys.exit(app.exec_())