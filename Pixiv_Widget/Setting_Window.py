#!/usr/bin/env python3
#自定义设置界面
import sys
sys.path.append('.')

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QFrame
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPixmap

from qtcreatorFile import settings_window
from utils.Project_Setting import setting


import cgitb
cgitb.enable(format='text', logdir='log_file')
class setting_window(QMainWindow, settings_window.Ui_SettingWindow):
    """docstring for setting_window"""
    _closed = pyqtSignal(dict)
    def __init__(self, parent, info):
        super(setting_window, self).__init__(parent)
        self._parent = parent
        self.setupUi(self)
        
        self.info = info
        self.cfg = setting()
        self.check_info()
        self.myset()    # 读取配置
        self.setFixedSize(self.width(), self.height())
        self.action_to_command()
        #self.scrollArea.horizontalScrollBar().setVisible(False)
        self._setting = {}
        self.move_self_to_center()

    def move_self_to_center(self):
        parent_x = self._parent.x()
        parent_y = self._parent.y()
        parent_w = self._parent.width()
        parent_h = self._parent.height()
        width = self.width()
        height = self.height()

        x = (parent_w - width)//2
        y = (parent_h - height)//2
        self.move(x+parent_x, y+parent_y)

    def check_info(self):
        key = []

    # 链接按钮与操作
    def action_to_command(self):
        self.setDefaultButton.clicked.connect(self.set_settings_default)
        self.setDefaultButton.clicked.connect(self.myset)
        self.setCacheButton.clicked.connect(lambda: self.setFilePath(self.cache_lineEdit))
        self.setSaveButton.clicked.connect(lambda: self.setFilePath(self.save_lineEdit))

    # 重置按钮执行重置配置操作
    def set_settings_default(self):
        self.cfg = setting()
        self.cfg.set_settings_default()
        self.cfg.get_setting()
        self.myset()

    # 修改缓存文件或保存文件的路径
    def setFilePath(self, lineEdit):
        now_path = '/'.join(lineEdit.text().split('/')[:-1])
        self.path = QFileDialog.getExistingDirectory(self, "浏览", now_path)
        lineEdit.setReadOnly(False)
        lineEdit.setText(self.path)
        lineEdit.setReadOnly(True)

    # 读取配置信息并显示
    def myset(self):
        self.cache_lineEdit.setReadOnly(False)
        self.cache_lineEdit.setText(self.cfg.temp_path)
        self.cache_lineEdit.setReadOnly(True)
        self.save_lineEdit.setReadOnly(False)
        self.save_lineEdit.setText(self.cfg.save_path)
        self.save_lineEdit.setReadOnly(True)
        if self.cfg.big_pic_size == 'large':
            self.big_radioButton.setChecked(True)
        elif self.cfg.big_pic_size == 'medium':
            self.middle_radioButton.setChecked(True)
        elif self.cfg.big_pic_size == 'square_medium':
            self.small_radioButton.setChecked(True)

        self.r18_checkBox.setChecked(self.cfg.has_r18)

        for i in range(3, 8):
            self.everyRowPicNumComboBox.addItem(str(i))
        self.everyRowPicNumComboBox.setCurrentText(str(self.cfg.per_row_pic_num))
        self.every_time_show_pic_num_lineEdit.setText(str(self.cfg.every_time_show_pic_num))

        self.update()

    # 配置生效
    def set_user_settings(self):
        temp_path = self.cache_lineEdit.text().strip()
        if not temp_path:
            temp_path = self.cfg.temp_path
        save_path = self.save_lineEdit.text().strip()
        if not save_path:
            save_path = self.cfg.save_path

        per_row_pic_num = self.everyRowPicNumComboBox.currentText()
        if self.r18_checkBox.isChecked():
            has_r18 = 'True'
        else:
            has_r18 = 'False'
        if self.big_radioButton.isChecked():
            big_pic_size = 'large'
        elif self.middle_radioButton.isChecked():
            big_pic_size = 'medium'
        elif self.small_radioButton.isChecked():
            big_pic_size = 'square_medium'

        every_time_show_pic_num = self.every_time_show_pic_num_lineEdit.text()
        
        self._setting['save_path'] = save_path
        self._setting['per_row_pic_num'] = int(per_row_pic_num)
        self._setting['has_r18'] = has_r18
        self._setting['big_pic_size'] = big_pic_size
        self._setting['every_time_show_pic_num'] = every_time_show_pic_num
        self._setting['temp_path'] = temp_path


    def closeEvent(self, qevent):
        self.set_user_settings()
        per_row_pic_num = self._setting['per_row_pic_num']
        h = self._parent.height()
        self._parent.resize(240*per_row_pic_num+135, h)
        setting = self._setting
        self.cfg.set_user_setting(setting)
        self._closed.emit(setting)

    def paintEvent(self, qevent):
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        widget_height = 0
        widget_width = self.scrollArea.width() - self.scrollArea.verticalScrollBar().width() - 2
        for i in self.scrollAreaWidgetContents.children():
            if isinstance(i, QFrame):
                widget_height += i.height()
        self.scrollAreaWidgetContents.resize(widget_width, widget_height)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication

    p = QApplication(sys.argv)

    key = ['big_pic_size', 'per_row_pic_num', 'temp_path', 'save_path','has_r18', 'every_time_show_pic_num']

    info = {}
    info['big_pic_size'] = 'large'
    info['per_row_pic_num'] = 4
    info['temp_path'] = '.'
    info['save_path'] = '.'
    info['has_r18'] = False
    info['every_time_show_pic_num'] = 20

    a = setting_window(parent=None, info=info)
    a.closeEvent = lambda x: print("nice")
    a.show()
    sys.exit(p.exec_())