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

FILE = '\033[31mPixiv_Login\033[0m'
class app_login(QMainWindow, pixiv_login_1.Ui_LoginMainWindow):
    login_timeout = 5000 #登录时长超过这个数之后显示退出按钮
    login_signal = pyqtSignal(dict)
    def __init__(self):
        super(app_login, self).__init__()
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

        self.prepared_num = 0
        self.loginToken = None

        # 指示获取hosts成功的数量
        self.require_hosts_num = 0

        # 当获取hosts成功的数量为3，表示所有hosts以获取成功，
        # 此时为True
        self._require_hosts_complete = False

        self.initThread1 = base_thread(parent=self, method=self.require_appapi_hosts, attr="pximg", url='i.pximg.net')
        self.initThread1.finish.connect(self.require_hosts_complete)
        self.initThread1.start()
        self.GIF.start()

        self.initThread2 = base_thread(parent=self, method=self.require_appapi_hosts, attr="hosts", url='public-api.secure.pixiv.net')
        self.initThread2.finish.connect(self.require_hosts_complete)
        self.initThread2.start()
        self.GIF.start()

        self.initThread3 = base_thread(parent=self, method=self.require_appapi_hosts, attr="default_head", url='s.pximg.net')
        self.initThread3.finish.connect(self.require_hosts_complete)
        self.initThread3.start()
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
        

    def require_appapi_hosts(self, attr, url):
        import time

        _time = 0
        while _time <= 6:
            try:
                setattr(self.api, attr, self.api.require_appapi_hosts(url))
            except:
                _time += 1
            else:
                print(f'{FILE}: Completely require_appapi_hosts: {url}')
                return {'is_success': True}

            time.sleep(1)
        
        return {'is_success': False, 'check_url': url}

    def require_hosts_complete(self, result):
        if not result['is_success']:
            self.EXIT = app_logout(self, isLogout=False)
            self.EXIT.show()
            print(f"{FILE}: require {result['check_url']} failed.")
            return
            
        self.require_hosts_num += 1
        if self.require_hosts_num >= 3:
            self._require_hosts_complete = True

    def pre_initUi(self, result):
        self.prepared_num += 1
        if 'token' in result:
            self.loginToken = result['token']
            self.auto = result['auto']
            self.username = result['login_account']
            self.lineEdit.setText(self.username)

        if self.prepared_num >= 2:
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

    def action_to_command(self):
        self.pushButton.clicked.connect(self.sub_login)
        self.pushButton.clicked.connect(self.startGIF)

    def auto_login(self):
        self.login_time_counter.start(self.login_timeout)
        self.loginText.setText('自动登录...')
        self.autoThread = base_thread(self, self._login, token_login=True)
        self.autoThread.finish.connect(self.isLoginSuccess)
        self.autoThread.wait()
        self.autoThread.start()

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
                'api': self.api,
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
        self.login_time_counter.start(self.login_timeout)   # 登录时间计时器重新计时
        self.loginText.setText('登录中...')
        self.login = base_thread(self, self._login, password_login=True)
        self.login.finish.connect(self.isLoginSuccess)
        self.login.wait()
        self.login.start()

    def startGIF(self):
        self.autoLogin_2.setVisible(True)
        self.GIF.start()

    def _login(self, password_login=False, token_login=False):
        while 1:
            if self._require_hosts_complete:
                self.username = self.lineEdit.text() if password_login else None
                password = self.lineEdit_2.text() if password_login else None
                refresh_token = self.loginToken if token_login else None
                try:
                    response = self.api.auth(username=self.username, password=password, refresh_token=refresh_token)
                except pixivpy3.utils.PixivError as e:
                    print(f"{FILE}: {e}")
                    return {'failed_text': '账号或密码错误！', 'login': False}
                else:
                    response['login'] = True
                    return response
            else:
                time.sleep(0.5)

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
    closed = pyqtSignal(dict)

    def __init__(self, parent, isLogout=True):
        super(app_logout, self).__init__(parent)
        self.setupUi(self)
        self._parent = parent
        self.action_to_command()
        self.isLogout = isLogout
        self.info = {'LOGOUT': False}
        self.login_info_parser = login_info_parser()
        if not isLogout:
            # 登录界面时初始化失败
            self.label.setText('初始化失败！重启程序或许可以解决问题！')
            self.label.setWordWrap(True)
            self.setWindowTitle('初始化失败')
        else:
            self.login_info_parser = login_info_parser()
            self.setWindowTitle('注销')
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
        access_token = self.login_info_parser.get_token()['token']
        try:
            self.login_info_parser.update_token(pixiv_id=1, user='', access_token=access_token, next_time_auto_login=0, login_account=None)
        except Exception as e:
            print(f"{FILE}: {e}")

        self.info['LOGOUT'] = True
        self.close()        
        
    def disagree(self):
        self.close()

    def closeEvent(self, qevent):
        self.closed.emit(self.info)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = app_login()
    # a.lineEdit.setReadOnly(True)
    # a.lineEdit_2.setReadOnly(True)
    a.move(2000, 1000)
    a.show()
    sys.exit(app.exec_())
