#!/usr/bin/env python3
#自定义设置界面

from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import pyqtSignal

from qtcreatorFile import settings_window


import cgitb
cgitb.enable(format='text', logdir='log_file')
class setting_window(QMainWindow, settings_window.Ui_MainWindow):
    """docstring for setting_window"""
    _closed = pyqtSignal(dict)
    def __init__(self, parent, info):
        super(setting_window, self).__init__(parent)
        self._parent = parent
        self.setupUi(self)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.resize(798, 1000)
        self.info = info
        self.check_info()
        self.myset()    # 读取配置
        self.setFixedSize(self.width(), self.height())
        self.action_to_command()
        self._setting = {}

    def check_info(self):
        key = ['big_pic_size', 'per_row_pic_num', 'temp_path', 'save_path','has_r18', 'every_time_show_pic_num']
        need_key = []
        need_not_key = []
        for i in self.info:
            if i not in key:
                need_not_key.append(i)
        for i in key:
            if i not in self.info:
                need_key.append(i)
        if need_key or need_not_key:
            raise KeyError(f"small_pic_frame doesn't need {need_not_key} and need {need_key}")

    # 链接按钮与操作
    def action_to_command(self):
        self.setDefaultButton.clicked.connect(self.set_settings_default)
        self.setDefaultButton.clicked.connect(self.myset)
        self.setCacheButton.clicked.connect(lambda: self.setFilePath(self.cache_lineEdit))
        self.setSaveButton.clicked.connect(lambda: self.setFilePath(self.save_lineEdit))

    # 重置按钮执行重置配置操作
    def set_settings_default(self):
        from utils.Project_Setting import setting

        cfg = setting()
        cfg.set_settings_default()
        cfg.get_setting()
        self.info['big_pic_size'] = cfg.big_pic_size
        self.info['per_row_pic_num'] = cfg.per_row_pic_num
        self.info['temp_path'] = cfg.temp_path
        self.info['save_path'] = cfg.save_path
        self.info['has_r18'] = cfg.has_r18
        self.info['every_time_show_pic_num'] = cfg.every_time_show_pic_num
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
        big_pic_size = self.info['big_pic_size']
        per_row_pic_num = self.info['per_row_pic_num']
        temp_path = self.info['temp_path']
        save_path = self.info['save_path']
        has_r18 = self.info['has_r18']
        every_time_show_pic_num = self.info['every_time_show_pic_num']

        self.cache_lineEdit.setReadOnly(False)
        self.cache_lineEdit.setText(temp_path)
        self.cache_lineEdit.setReadOnly(True)
        self.save_lineEdit.setReadOnly(False)
        self.save_lineEdit.setText(save_path)
        self.save_lineEdit.setReadOnly(True)
        if big_pic_size == 'large':
            self.big_radioButton.setChecked(True)
        elif big_pic_size == 'medium':
            self.middle_radioButton.setChecked(True)
        elif big_pic_size == 'square_medium':
            self.small_radioButton.setChecked(True)
        if has_r18:
            self.r18_checkBox.setChecked(True)
        else:
            self.r18_checkBox.setChecked(False)
        for i in range(3, 8):
            self.everyRowPicNumComboBox.addItem(str(i))
        self.everyRowPicNumComboBox.setCurrentText(str(per_row_pic_num))
        self.every_time_show_pic_num_lineEdit.setText(str(every_time_show_pic_num))

        self.update()

    # 配置生效
    def set_user_settings(self):
        temp_path = self.cache_lineEdit.text()
        save_path = self.save_lineEdit.text()
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
        
        self._setting['temp_path'] = temp_path
        self._setting['save_path'] = save_path
        self._setting['per_row_pic_num'] = int(per_row_pic_num)
        self._setting['has_r18'] = has_r18
        self._setting['big_pic_size'] = big_pic_size
        self._setting['every_time_show_pic_num'] = every_time_show_pic_num


    def closeEvent(self, qevent):
        self.set_user_settings()
        per_row_pic_num = self._setting['per_row_pic_num']
        h = self._parent.height()
        self._parent.resize(240*per_row_pic_num+200, h)
        setting = self._setting
        self._closed.emit(setting)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys

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
    a.show()
    sys.exit(p.exec_())