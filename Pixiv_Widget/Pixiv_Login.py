#!/usr/bin/env python3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt5.QtGui import QIcon, QPalette, QBrush, QMovie, QPixmap
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
import pixivpy3

import sys
sys.path.append('.')

# qtcreator模块导入
from qtcreatorFile import pixiv_login_1
from qtcreatorFile import Pixiv_Logout

# 自定义模块导入
from utils.Process_Token import login_info_parser
from utils.Project_Setting import setting
from Pixiv_Api.My_Api import my_api
from Pixiv_Thread.My_Thread import base_thread

import time

import cgitb
cgitb.enable(format='text', logdir='log_file')
class app_login(QMainWindow, pixiv_login_1.Ui_LoginMainWindow):
    login_timeout = 5000 #登录时长超过这个数之后显示退出按钮
    login_signal = pyqtSignal(dict)
    def __init__(self, login_success):
        super(app_login, self).__init__()
        start = time.time()
        self.login_success = login_success
        self.cfg = setting()
        self.get_setting()
        self.login_info_parser = login_info_parser()
        self.api = my_api()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.set_style()
        self.reset_RES_dir()
        #self.widget.setStyleSheet("QWidget:{border-radius:3px}")
        #self.exit_button.setStyleSheet("QPushButton{border-image: url(./RES/exit.png)};")
        self.exit_button.clicked.connect(self.close)
        #self.interrupt_login_button.setStyleSheet("QPushButton{border-image: url(./RES/exit.png)};")
        self.interrupt_login_button.clicked.connect(self.relogin)
        self.interrupt_login_button.setVisible(False)
        self.setFixedSize(520, 431)
        self.setWindowIcon(QIcon(self.app_icon))
        self.setWindowTitle('Pixiv')
        self.GIF = QMovie(self.login_gif)
        self.loginGIF.setMovie(self.GIF)
        #self.add_background()
        self.lineEdit.setPlaceholderText('请输入账号')
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.api = my_api()

        self.prepared_num = 0

        self.initThread = base_thread(parent=self, method=self.require_appapi_hosts)
        self.initThread.finish.connect(self.pre_initUi)
        self.initThread.start()
        self.GIF.start()

        self.checkFileThread = base_thread(self, method=self.cfg.check_file)
        self.checkFileThread.finish.connect(self.pre_initUi)
        self.checkFileThread.start()

        self.getTokenThread = base_thread(self, method=self.login_info_parser.get_token)
        self.getTokenThread.finish.connect(self.pre_initUi)
        self.getTokenThread.start()

        self.loginText.setText('程序初始化中...')

        self.move_self_to_center()
        self.login_time_counter = QTimer()
        self.login_time_counter.timeout.connect(self.provide_escape_button)
        self.not_to_login = False   # 当为True时中断登录

        
        # 为了圆角时不产生黑色背景
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        ###

        self.drag = False

        print(time.time() - start, '>'*90)

    def reset_RES_dir(self):
        import shutil, os
        if not os.path.exists('RES'):
            os.mkdir('RES')
            dir_name = os.path.dirname(__file__)
            RES = f"{dir_name}/RES"
            for i in os.listdir(RES):
                shutil.copy(f'{RES}/{i}', f"./RES/{i}")


    def set_style(self):
        try:
            f = open('Login_Style.qss', encoding='utf-8')
        except:
            from utils import Reset_Style
            Reset_Style.reset_login_style()
            style = Reset_Style.LOGIN_STYLE
        else:
            style = f.read()
            f.close()
        self.setStyleSheet(style)

    def provide_escape_button(self):
        self.login_time_counter.stop()
        self.interrupt_login_button.setVisible(True)

    def relogin(self):
        self.not_to_login = True
        self.interrupt_login_button.setVisible(False)
        self.autoLogin_2.setVisible(False)

    def move_self_to_center(self):
        from PyQt5.QtWidgets import QDesktopWidget
        desktop_w = QDesktopWidget().width()
        desktop_h = QDesktopWidget().height()
        width = self.width()
        height = self.height()

        x = (desktop_w - width) // 2
        y = (desktop_h - height) // 2
        self.move(x, y)

    def get_setting(self):
        self.temp_path = self.cfg.temp_path
        self.save_path = self.cfg.save_path
        self.big_pic_size = self.cfg.big_pic_size
        self.timeout_pic = self.cfg.timeout_pic
        # self.loading_gif = self.cfg.loading_gif
        # self.login_background = self.cfg.login_background
        # self.main_window_background = self.cfg.main_window_background
        # self.font_color = self.cfg.font_color
        # self.font = self.cfg.font
        # self.press_color = self.cfg.press_color
        # self.focus_color = self.cfg.focus_color
        self.app_icon = self.cfg.app_icon
        # self.loading_big_gif = self.cfg.loading_big_gif
        self.login_gif = self.cfg.login_gif
        
        self.every_time_show_pic_num = self.cfg.every_time_show_pic_num
        self.tips_dot = self.cfg.tips_dot
        self.per_row_pic_num = self.cfg.per_row_pic_num
        self.timeout = self.cfg.timeout
        

    def require_appapi_hosts(self):
        import time

        _time = 0
        while _time <= 6:
            try:
                self.api.pximg = self.api.require_appapi_hosts("i.pximg.net")
                self.api.public_api = self.api.hosts = self.api.require_appapi_hosts("public-api.secure.pixiv.net")
            except:
                _time += 1
            else:
                print('Complete: require_appapi_hosts')
                return {'is_success': True}

            time.sleep(1)
        
        return {'is_success': False}

    def pre_initUi(self, result):
        self.prepared_num += 1
        if 'token' in result:
            self.loginToken = result['token']
            self.auto = result['auto']
            self.username = result['login_account']
            self.lineEdit.setText(self.username)
        elif 'is_success' in result and not result['is_success']:
            self.EXIT = app_logout(self, main=lambda: print(0), isLogout=False)
            self.EXIT.show()
            return
        if self.prepared_num >= 3:
            self.initUi()

    def initUi(self):
        self.api.set_accept_language('zh-cn')
        self.action_to_command()
        if self.loginToken and self.auto:
            self.startGIF()
            self.autoLogin.setChecked(True)
            self.auto_login()
        else:
            self.autoLogin_2.setVisible(False)

    # def add_background(self):
    #     import os
    #     if os.path.exists(self.login_background):
    #         window_pale = QPalette()
    #         window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap(self.login_background)))
    #         self.setPalette(window_pale)
    #     else:
    #         #self.setStyleSheet('background-color: rgb(86, 86, 86)')
    #         pass

    def action_to_command(self):
        self.pushButton.clicked.connect(self.sub_login)
        self.pushButton.clicked.connect(self.startGIF)

    def auto_login(self):
        self.login_time_counter.start(self.login_timeout)
        self.loginText.setText('自动登录...')
        self.autoThread = base_thread(self, self.sub_auto_login)
        self.autoThread.finish.connect(self.isLoginSuccess)
        self.autoThread.wait()
        self.autoThread.start()

    def sub_auto_login(self):
        try:
            response = self.api.auth(refresh_token=self.loginToken)
        except pixivpy3.utils.PixivError:
            self.autoLoginSuccess = False
            return {'failed_text': '自动登录失败', 'login': False}
        else:
            response['login'] = True
            return response

    def isLoginSuccess(self, response):
        if self.not_to_login:
            self.not_to_login = False
            return 
        if response['login']:
            if self.autoLogin.isChecked():
                self.auto = 1
            else:
                self.auto = 0

            ID = int(response['response']['user']['id'])
            USER = response['response']['user']['name']
            self.login_info_parser.update_token(pixiv_id=ID, user=USER, login_account=self.username,
                                                access_token=response['response']['refresh_token'],
                                                next_time_auto_login=self.auto)
            self.loginText.setText('登录成功')

            info = {
                'parent': self, 
                'ID': str(ID), 
                'USER': USER, 
                'user_head': response['response']['user']['profile_image_urls']['px_50x50'],
                'api': self.api
                }

            self.timer = QTimer()
            self.timer.timeout.connect(self.timer.stop)
            self.timer.timeout.connect(lambda: self.emit_login_signal(info))
            self.timer.start(500)

        else:
            self.loginText.setText(response['failed_text'])
            self.loginText.show()
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: [self.autoLogin_2.setVisible(False), self.timer.stop()])
            self.timer.start(500)

    def sub_login(self):
        self.login_time_counter.start(self.login_timeout)
        self.loginText.setText('登录中...')
        self.login = base_thread(self, self._login)
        self.login.finish.connect(self.isLoginSuccess)
        self.login.wait()
        self.login.start()

    def startGIF(self):
        self.autoLogin_2.setVisible(True)
        self.GIF.start()

    def _login(self):
        self.username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        try:
            response = self.api.login(username=self.username, password=password)
        except pixivpy3.utils.PixivError as e:
            return {'failed_text': '账号或密码错误！', 'login': False}
        else:
            response['login'] = True
            return response

    def keyPressEvent(self, qevent):
        if qevent.key() in [16777221, 16777220]:  # Enter
            if not self.loginGIF.isVisible():
                self.sub_login()
                self.startGIF()

        if qevent.key() == Qt.Key_S:
            self.set_style()

    def mousePressEvent(self, qevent):
        from PyQt5.QtCore import QSize
        if qevent.button() == 1 and qevent.x() in range(0, self.width()-30) and qevent.y() in range(0, 30):
            self.drag = True
            self.old_pos = qevent.pos()

    def mouseMoveEvent(self, qevent):
        if self.drag:
            diff_pos = qevent.pos() - self.old_pos
            self.move(self.pos() + diff_pos)

    def mouseReleaseEvent(self, qevent):
        self.drag = False

    def emit_login_signal(self, info):
        self.close()
        self.login_signal.emit(info)
        
class app_logout(QMainWindow, Pixiv_Logout.Ui_MainWindow):
    """docstring for app_logout"""
    closed = pyqtSignal()

    def __init__(self, parent, main, isLogout=True):
        super(app_logout, self).__init__(parent)
        self.setupUi(self)
        self._parent = parent
        self.action_to_command()
        self.isLogout = isLogout
        self.main = main
        if not isLogout:
            # 登录界面时初始化失败
            self.label.setText('初始化失败！重启程序或许可以解决问题！')
            self.label.setWordWrap(True)
        else:
            self.login_info_parser = login_info_parser()
        # self.setFixedSize(self.width(), self.height())
        self.move_self_to_center()

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

    def action_to_command(self):
        self.OKButton.clicked.connect(self.agree)
        self.cancelButton.clicked.connect(self.disagree)

    def agree(self):
        self._logout()


    def _logout(self):
        try:
            self.login_info_parser.update_token(pixiv_id=1, user='', access_token='', next_time_auto_login=0, login_account=None)
        except Exception as e:
            print(e)

        self._parent.close()
        self.close()
        self.main(_parent)
        
    def disagree(self):
        self.close()

    def closeEvent(self, qevent):
        self.closed.emit()
        del self


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = app_login(login_success=lambda x,y,z,j: print(''))
    a.lineEdit.setReadOnly(True)
    a.lineEdit_2.setReadOnly(True)
    a.move(2000, 1000)
    a.show()
    sys.exit(app.exec_())
