#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QBrush
from PyQt5.QtCore import QRect, Qt, QTimer
from PyQt5.Qt import QPropertyAnimation
from math import ceil
import sys
from PyQt5 import sip
import os
from memory_profiler import profile
import cgitb


# 导入qtcreator模块
from Pixiv_Widget.Search_Frame import search_frame
from qtcreatorFile import pixiv_main_window

# 导入自定义模块
from Pixiv_Widget.Info_Frame import info_frame
from Pixiv_Widget.My_Label import my_label
from Pixiv_Thread.My_Thread import base_thread
from Pixiv_Widget.Original_Pic import original_pic
from Pixiv_Widget.Setting_Window import setting_window
from Pixiv_Widget.Small_Pic_Frame import small_pic_frame
from utils.Project_Setting import setting
from Pixiv_Widget.Pixiv_Login import app_login
from Pixiv_Widget.Search_Frame import search_frame
from Pixiv_Widget.comment_widget import Comment_Widget
from Pixiv_Widget.illust_relate import Illust_Relate
from Pixiv_Widget.My_Widget import Scroll_Widget
from Pixiv_Widget.My_Widget import my_widget



cgitb.enable(format='text', logdir='log_file')


class main_pixiv(QMainWindow, pixiv_main_window.Ui_MainWindow):
    def __init__(self, api, user_id, username, user_pic_link):
        super(main_pixiv, self).__init__()
        #self.setStyleSheet("QToolTip{background-color: #000000; color: #FFFFFF; border: none}")
        base_thread.root = self
        self.api = api
        self.get_setting()
        self.setMinimumSize(917, 660 - 52)
        #self.setMinimumSize(1257, 811)
        self.setupUi(self)
        self.set_style()
        smallFrame_h = self.SmallFrame.height()
        # 为了得出tabbar的高度
        self.tabWidget.addTab(QWidget(), 'test_tab_bar_height')
        self.tabBar_h = self.tabWidget.tabBar().height()
        self.tabWidget.removeTab(0)
        ###
        tab_h = self.tabWidget.height()
        infoFrame_h = smallFrame_h - tab_h
        self.infoFrame = info_frame(self.SmallFrame, main=self, info={'temp_path': self.temp_path, 'timeout_pic': self.timeout_pic})
        self.infoFrame.setGeometry(QRect(0, 730, 1041, infoFrame_h))
        self.searchFrame = search_frame(self.SmallFrame, main=self)
        self.searchFrame.setGeometry(QRect(0, -120, 1041, 120))

        self.setWindowIcon(QIcon(self.app_icon))
        self.setWindowTitle('Pixiv')
        self.tab = {}
        # self.tabWidget.setStyleSheet(
        #     "QTabWidget:pane{background-color: transparent;border:none;}\nQTabBar:tab{color:rgb(255, 255, 255); background-color: rgba(102, 206, 255, 128)}\nQTabBar:tab:selected{background-color: rgba(102, 206, 255, 255)}")
        #self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_tab)
        self.tabWidget.currentChanged['int'].connect(self.change_tab)

        ### 设置用户名
        self.usernameLabel = my_label(self.frame, {'tag': user_id, 'text': username})  # 左上角用户名
        self.usernameLabel.clicked.connect(self.show_action)
        self.usernameLabel.setGeometry(QRect(2, 50, len(username) * 20, 41))
        # self.usernameLabel.setWordWrap(True)
        self.usernameLabel.setObjectName("usernameLabel")
        self.usernameLabel.setText(username)
        ###

        file_name = f"user_{user_id}_pic"
        self.user_pic_thread = base_thread(self, self.api.cache_pic, url=user_pic_link, file_name=file_name,
                                           path=self.temp_path, info={'file_name': file_name, 'url': user_pic_link,
                                                                      'label': 'self.login_user_pic_label', 'row': 53})
        self.user_pic_thread.finish.connect(self.load_user_head)
        # self.user_pic_thread.finish.connect(self.user_pic_thread.disconnect)
        self.user_pic_thread.wait()
        self.user_pic_thread.start()


        desktop = QApplication.desktop()
        screen_rect = desktop.screenGeometry()
        height = screen_rect.height()

        picture = QPixmap(self.tips_dot)
        self.downloadTipsLabel.setPixmap(picture)
        self.downloadTipsLabel.setVisible(False)
        self.DownloadPageScroll.setVisible(False)
        # 显示大图时才可以出现
        self.infoFrame.saveButton.setVisible(False)
        self.infoFrame.titleText.setVisible(False)
        self.infoFrame.authText.setVisible(False)
        self.infoFrame.text_scroll.setVisible(False)
        self.bigPicScrollArea.setVisible(False)
        if hasattr(self, 'comment_widget'):
            self.comment_widget.setVisible(False)
        ###

        self.rank_pic_s = {}  # title标签下的第n张小图片
        self.big_pic = 0  # 第n张大图片
        self.frames = {}
        self.small_pic_frame_animation = {}  # 预览图动画
        self.bigFrames = {}
        self.threads = {}  # 存储线程
        self.next_url_s = {}  # title标签的next_url
        self.method = 'illust_recommended0'  # 指示当前显示的板块
        self.title_box = []  # 存放已存在的标签
        self.mode = ''  # 该属性已名存实亡

        self.now_per_row_pic_num = self.per_row_pic_num
        self.baseThread = {}
        self.now_page = 'show_pic'
        #self.downloadNum = 0  # 下载数，用于下载页面的排版（待增加下载页）
        self.downloadTimer = {}
        self.pbar = {}
        self.downloadThreads = {}
        self.cache_item_box = {}
        #self.add_background()
        self.R18Button.setVisible(self.has_r18)
        self.create_download_view()
        self.progressThreads = {}
        self.tab_title = ''
        self.action_to_command()  # 链接事件和函数
        self.show_original_threads = {}
        self.sub_windows = {}

        self.scrollAreas = {}
        self.scrollAreaWidgetContents = {}
        width = 240 * self.per_row_pic_num + 135
        self.resize(width, int(height * 0.75))

        self.move_self_to_center()  # 移动窗口到中央
        self.show()

        self.ajust_cate_widget_size()  # 调整左侧类别按钮（推荐、每日...）的容器的大小
        self.show_pic('illust_recommended', title='推荐', isMoreButton=False, flag='推荐')

    def move_self_to_center(self):
        from PyQt5.QtWidgets import QDesktopWidget
        desktop_w = QDesktopWidget().width()
        desktop_h = QDesktopWidget().height()
        width = self.width()
        height = self.height()

        x = (desktop_w - width) // 2
        y = (desktop_h - height) // 2
        self.move(x, y)

    def ajust_cate_widget_size(self):
        command_button_num = 0
        for i in self.cate_widget.children():
            if isinstance(i, QWidget) and i.isVisible():
                command_button_num += 1
                button = i
        button_h = button.height()
        cate_widget_w = self.cate_widget.width()
        self.cate_widget.resize(cate_widget_w, button_h * command_button_num)

    def show_info(self):
        from Pixiv_Widget.Info_Window import _info_window
        def del_info_window():
            del self.info_window

        if hasattr(self, 'info_window'):
            self.info_window.show()
        else:
            self.info_window = _info_window(parent=self)
            self.info_window.closed.connect(del_info_window)
            self.info_window.setWindowTitle('哟！')
            self.info_window.setWindowIcon(QIcon(self.app_icon))
            self.info_window.show()

    def get_setting(self):
        cfg = setting()
        self.temp_path = cfg.temp_path
        self.save_path = cfg.save_path
        self.big_pic_size = cfg.big_pic_size
        self.timeout_pic = cfg.timeout_pic
        self.loading_gif = cfg.loading_gif
        self.login_background = cfg.login_background
        self.main_window_background = cfg.main_window_background
        self.font_color = cfg.font_color
        self.font = cfg.font
        self.press_color = cfg.press_color
        self.focus_color = cfg.focus_color
        self.app_icon = cfg.app_icon
        self.loading_big_gif = cfg.loading_big_gif
        self.login_gif = cfg.login_gif
        self.has_r18 = cfg.has_r18
        self.every_time_show_pic_num = cfg.every_time_show_pic_num
        self.tips_dot = cfg.tips_dot
        self.per_row_pic_num = cfg.per_row_pic_num
        self.timeout = cfg.timeout
        self.no_h = cfg.no_h

    def show_action(self, info):
        from PyQt5.QtWidgets import QMenu
        from PyQt5.QtGui import QCursor
        user_id = info['tag']

        # 用户关注
        用户关注 = """base_thread(self, self.api.user_following,
            info={'title': title},
            user_id=%s,
            )""" % user_id

        # 用户粉丝
        用户粉丝 = """base_thread(self, self.api.user_follower,
            info={'title': title},
            user_id=%s,
            )""" % user_id

        # 用户好友
        用户好友 = """base_thread(self, self.api.user_mypixiv,
            info={'title': title},
            user_id=%s,
            )""" % user_id

        self.qmenu = QMenu()
        myIllusts = self.qmenu.addAction('我的作品')
        myIllusts.triggered.connect(lambda x: self.user_illusts({'user_id': user_id, 'title': '我的作品'}))

        myCollection = self.qmenu.addAction('我的收藏')
        myCollection.triggered.connect(lambda x: self.show_pic(_mode={'user_id': user_id}, title='我的收藏', flag='收藏作品'))

        myFollow = self.qmenu.addAction('我的关注')
        myFollow.triggered.connect(
            lambda x: self.search_user(_mode={'user_id': user_id, 'Thread': 用户关注}, title='我的关注', isSearch=False))

        myFans = self.qmenu.addAction('我的粉丝')
        myFans.triggered.connect(
            lambda x: self.search_user(_mode={'user_id': user_id, 'Thread': 用户粉丝}, title='我的粉丝', isSearch=False))

        myFriends = self.qmenu.addAction('我的好友')
        myFriends.triggered.connect(
            lambda x: self.search_user(_mode={'user_id': user_id, 'Thread': 用户好友}, title='我的好友', isSearch=False))

        myBlackList = self.qmenu.addAction('我的黑名单')

        self.qmenu.exec(QCursor.pos())

    #@profile
    def close_tab(self, index):
        from PyQt5 import sip
        def try_pop(_dict, item):
            try:
                _dict[item].deleteLater()
            except:
                pass
            else:
                sip.delete(_dict[item])
            try:
                _dict.pop(item)
            except KeyError:
                pass
            return _dict

        title = self.tabWidget.tabText(index)
        self.tabWidget.removeTab(index)
        try_pop(self.cache_item_box, title)
        try_pop(self.tab, title)
        try_pop(self.scrollAreaWidgetContents, title)
        try_pop(self.scrollAreas, title)
        try_pop(self.rank_pic_s, title)
        try_pop(self.next_url_s, title)
        try_pop(self.frames, title)

    def change_tab(self, index):
        self.tab_title = title = self.tabWidget.tabText(index)
        self.infoFrame.moreButton.disconnect()
        if title == '':
            return
        flag = self.tab[title].flag
        if flag == '用户':
            self.infoFrame.moreButton.clicked.connect(lambda: self._search(self.next_url_s[title], title))
        else:
            self.infoFrame.moreButton.clicked.connect(
                lambda: self.show_pic(self.method, self.next_url_s[title], title, flag=flag))
        try:
            if self.next_url_s[title]:
                self.infoFrame.moreButton.setText('更多')
            else:
                self.infoFrame.moreButton.setText('没有更多了')
        except KeyError:
            self.infoFrame.moreButton.setText('更多')

    def create_download_view(self):
        # 创建下载页面的表
        from Pixiv_Widget.myTableView import TableView
        self.table = TableView(self.SmallFrame)
        width = self.SmallFrame.width()
        self.table.setGeometry(QRect(0, 0, width, 731))
        self.table.setupUi()
        self.table.setVisible(False)

    def add_background(self):
        from PyQt5.QtGui import QPalette
        if os.path.exists(self.main_window_background):
            window_pale = QPalette()
            window_pale.setBrush(self.backgroundRole(), QBrush(QPixmap(self.main_window_background)))
            self.setPalette(window_pale)
        else:
            #self.setStyleSheet('background-color: rgb(0, 0, 0)')
            pass

    def rebuild(self, title):
        h = self.tabWidget.height()
        w = self.tabWidget.width()
        tabBar_h = self.tabWidget.tabBar().height()
        self.scrollAreas[title] = QScrollArea(self.tab[title])
        self.scrollAreas[title].setGeometry(QRect(0, 0, w-3, h-self.tabBar_h))
        #self.scrollAreas[title].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.scrollAreas[title].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollAreas[title].setWidgetResizable(False)
        self.scrollAreas[title].setObjectName("scrollArea")
        self.scrollAreas[title].verticalScrollBar().valueChanged.connect(lambda x: self.slideDown(x, title))

        smallFrame_w = self.SmallFrame.width()
        self.scrollAreaWidgetContents[title] = my_widget()
        self.scrollAreaWidgetContents[title].setGeometry(QRect(0, 0, smallFrame_w - 20, 200))
        self.scrollAreaWidgetContents[title].setObjectName("scrollAreaWidgetContent")
        self.scrollAreas[title].setWidget(self.scrollAreaWidgetContents[title])

    def slideDown(self, x, title):
        m = self.scrollAreas[title].verticalScrollBar().maximum()
        if m - x <= 411*1.5:
            self.infoFrame.moreButton.click()

    def show_pic(self, method='', _mode={}, title=None, isMoreButton=True, flag=''):
        from Pixiv_Widget.My_Widget import my_widget

        if _mode == None:
            self.infoFrame.moreButton.setText('没有更多了')
            return
        else:
            self.infoFrame.moreButton.setText('更多')
        if self.infoFrame.detail_is_show():  # 复原详情
            self.infoFrame.hide_illust_detail()

        ## 先返回图片浏览
        self.escapeDownloadPage(self.now_page)
        self.now_page = 'show_pic'
        self.returnSmallPic()
        self.searchFrame.hide_search_frame()
        ###

        # 点击左边按钮时，查找已存在的窗口并切换到该窗口
        if title in self.tab and not isMoreButton:
            _tab_index = 0
            for _tab in self.tab:
                if _tab == title:
                    self.tabWidget.setCurrentIndex(_tab_index)
                    return
                _tab_index += 1
        ### 

        if title not in self.tab:
            self.tabWidget.setVisible(True)
            self.tab[title] = my_widget(flag=flag)
            self.tab[title].set_loading(False)
            ##self.tab[title].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            self.tab[title].setObjectName("tab")

            # h = self.tabWidget.height()
            # w = self.tabWidget.width()
            # self.scrollAreas[title] = QScrollArea(self.tab[title])
            # self.scrollAreas[title].setGeometry(QRect(0, 0, w - 3, h - 32))
            # #self.scrollAreas[title].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            # self.scrollAreas[title].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # self.scrollAreas[title].setWidgetResizable(False)
            # self.scrollAreas[title].setObjectName("scrollArea")
            self.rebuild(title)
            self.tabWidget.addTab(self.tab[title], title)
            self.infoFrame.moreButton.disconnect()
            self.infoFrame.moreButton.clicked.connect(
                lambda: self.show_pic(self.method, self.next_url_s[title], title=title, flag=flag))
            self.tab_title = title
            self.tabWidget.setCurrentIndex(len(self.tab) - 1)

            self.method = method
            self.title_box.append(title)
            self.rank_pic_s[title] = 0
            self.threads = {}
            self.frames[title] = {}  # title窗口下的frames
            self.cache_item_box[title] = []
            self.small_pic_frame_animation[title] = {}  # 预览图动画

        if not self.cache_item_box[title]:
            _filter = _mode.get('filter', 'for_ios')
            offset = _mode.get('offset', None)

            if flag == '推荐':
                content_type = _mode.get("content_type", 'illust')
                include_ranking_label = _mode.get("include_ranking_label", True)
                min_bookmark_id_for_recent_illust = _mode.get("min_bookmark_id_for_recent_illust", None)
                max_bookmark_id_for_recommend = _mode.get("max_bookmark_id_for_recommend", None)
                include_ranking_illusts = _mode.get("include_ranking_illusts", None)
                include_privacy_policy = _mode.get("include_privacy_policy", None)
                bookmark_illust_ids = _mode.get("bookmark_illust_ids", None)
                self.baseThread['get_img_info'] = base_thread(self, self.api.illust_recommended,
                                                              info={'title': title},
                                                              content_type=content_type,
                                                              include_ranking_label=include_ranking_label,
                                                              filter=_filter,
                                                              max_bookmark_id_for_recommend=max_bookmark_id_for_recommend,
                                                              min_bookmark_id_for_recent_illust=min_bookmark_id_for_recent_illust,
                                                              offset=offset,
                                                              include_ranking_illusts=include_ranking_illusts,
                                                              bookmark_illust_ids=bookmark_illust_ids,
                                                              include_privacy_policy=include_privacy_policy)

            elif flag == '排行榜':
                mode = _mode.get('mode', 'day')
                date = _mode.get('date', None)
                self.baseThread['get_img_info'] = base_thread(self, self.api.illust_ranking,
                                                              info={'title': title},
                                                              mode=mode,
                                                              filter=_filter,
                                                              date=date,
                                                              offset=offset,
                                                              )

            # 标签
            elif flag == '标签作品':
                word = _mode['word']
                print(word)
                search_target = _mode.get("search_target", 'partial_match_for_tags')
                sort = _mode.get("sort", 'date_desc')
                duration = _mode.get("duration", None)
                self.baseThread['get_img_info'] = base_thread(self, self.api.search_illust,
                                                              info={'title': title},
                                                              word=word,
                                                              search_target=search_target,
                                                              sort=sort,
                                                              duration=duration,
                                                              filter=_filter,
                                                              offset=offset
                                                              )

            # 画师作品
            elif flag == '用户作品':
                user_id = _mode['user_id']
                _type = _mode.get('type', 'illust')
                _filter = _mode.get('filter', 'for_ios')
                self.baseThread['get_img_info'] = base_thread(self, self.api.user_illusts,
                                                              info={'title': title},
                                                              user_id=user_id,
                                                              type=_type,
                                                              filter=_filter,
                                                              offset=offset
                                                              )

            # 用户收藏
            elif flag == '收藏作品':
                user_id = _mode['user_id']
                restrict = _mode.get('restrict', 'public')
                max_bookmark_id = _mode.get('max_bookmark_id', None)
                tag = _mode.get('tag', None)
                self.baseThread['get_img_info'] = base_thread(self, self.api.user_bookmarks_illust,
                                                              info={'title': title},
                                                              user_id=user_id,
                                                              restrict=restrict,
                                                              filter=_filter,
                                                              max_bookmark_id=max_bookmark_id,
                                                              tag=tag
                                                              )
            elif flag == '作品id':
                illust_id = _mode['illust_id']
                self.baseThread['get_img_info'] = base_thread(self, self.api.illust_detail,
                                                              info={'_title': title},
                                                              illust_id=illust_id,
                                                              )

            self.baseThread['get_img_info'].finish.connect(self.parse_pic_info)
            self.baseThread['get_img_info'].wait()
            self.baseThread['get_img_info'].start()
        else:
            self.parse_pic_info({"title": title, 'load_cache': True})

    def parse_pic_info(self, ranking={}):
        from PyQt5.QtCore import QRect
        if 'ERROR' in ranking or 'error' in ranking:    # 网络错误, 重新请求
            method = ranking['method']
            args = ranking['args']
            info = ranking['info']
            self.baseThread['get_img_info'] = base_thread(self, method,
                                                              info=info,
                                                              **args,
                                                              )
            self.baseThread['get_img_info'].finish.connect(self.parse_pic_info)
            self.baseThread['get_img_info'].wait()
            self.baseThread['get_img_info'].start()
            title = ranking['info']['title']
            self.scrollAreaWidgetContents[title].add_load_time(1)

            return

        if 'next_url' not in ranking and not ranking.get('load_cache', False):       # 搜索作品id时没有next_url, 因此需判断
            ranking = self.add_key_to_result(ranking)

        title = ranking['title']  # tab_title

        # 获取图片信息时，就把当前窗口关闭会引发KeyError异常，因此需要判断
        if title not in self.cache_item_box:
            return
        self.scrollAreaWidgetContents[title].set_loading(False)
        try:
            self.baseThread['get_img_info'].disconnect()
        except:
            pass

        if not self.cache_item_box[title]:
            try:        # 获取图片信息时触发网络错误会导致ranking没有illusts键
                self.cache_item_box[title] = ranking['illusts']
            except KeyError:
                return
            self.next_url_s[title] = self.api.parse_qs(ranking['next_url'])

        ranking = self.cache_item_box[title][:self.every_time_show_pic_num]  # 每次点击最多只加载self.every_time_show_pic_num张图片（适用于小图浏览）

        x = {0: 0, 1: 240, 2: 480, 3: 720, 4: 960, 5: 1200, 6: 1440, 7: 1680, 8: 1920, 9: 2160}
        for i in ranking:
            info = {}
            illust_id = i['id']
            info['illust'] = i
            info['api'] = self.api
            info['loading_gif'] = self.loading_gif
            info['timeout_pic'] = self.timeout_pic
            info['temp_path'] = self.temp_path
            info['start_row'] = int(self.table.model().rowCount() / self.per_row_pic_num)#int(self.downloadNum / self.per_row_pic_num)
            info['save_path'] = self.save_path
            info['has_r18'] = self.has_r18
            info['no_h'] = self.no_h
            info['main'] = self

            small_pic_frame_x = x[self.rank_pic_s[title] % self.now_per_row_pic_num]
            small_pic_frame_y = ((self.rank_pic_s[title] // self.now_per_row_pic_num)) * 411

            self.frames[title][illust_id] = small_pic_frame(self.scrollAreaWidgetContents[title], info=info)
            self.frames[title][illust_id].progress.connect(self.create_download_progress)
            self.frames[title][illust_id].pic_click.connect(self.show_big_pic)
            self.frames[title][illust_id].show()
            self.small_pic_frame_animation[title][illust_id] = QPropertyAnimation(self.scrollAreaWidgetContents[title])
            self.small_pic_frame_animation[title][illust_id].setPropertyName(b'geometry')
            self.small_pic_frame_animation[title][illust_id].setTargetObject(self.frames[title][illust_id])
            self.small_pic_frame_animation[title][illust_id].setStartValue(
                QRect(small_pic_frame_x, small_pic_frame_y, 0, 0))
            self.small_pic_frame_animation[title][illust_id].setEndValue(
                QRect(small_pic_frame_x, small_pic_frame_y, 234, 405))
            self.small_pic_frame_animation[title][illust_id].setDuration(200)
            self.small_pic_frame_animation[title][illust_id].start()

            if (self.rank_pic_s[title] + 1) % self.now_per_row_pic_num == 1:
                self.scrollAreaWidgetContents[title].resize(self.now_per_row_pic_num * 240, (
                    ceil((self.rank_pic_s[title] + 1) / self.now_per_row_pic_num)) * 411)
            self.rank_pic_s[title] += 1

            self.cache_item_box[title].pop(self.cache_item_box[title].index(i))
        self.test()

    def action_to_command(self):
        # 链接操作与函数
        self.RankButton.clicked.connect(
            lambda: self.show_pic('+illust_ranking', {'mode': 'day'}, title='日排行榜', isMoreButton=False, flag='排行榜'))
        self.recommendButton.clicked.connect(
            lambda: self.show_pic('illust_recommended', title='推荐', isMoreButton=False, flag='推荐'))
        self.logoutButton.clicked.connect(self._logout)
        self.dayFemaleButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 1}', {'mode': 'day_female'}, title='日排行榜：女',
                                  isMoreButton=False, flag='排行榜'))
        self.dayMaleButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 2}', {'mode': 'day_male'}, title='日排行榜：男', isMoreButton=False,
                                  flag='排行榜'))
        self.dayMangaButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 3}', {'mode': 'day_manga'}, title='日排行榜：漫画',
                                  isMoreButton=False, flag='排行榜'))
        self.dayRookieButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 4}', {'mode': 'week_rookie'}, title='周排行榜：新人',
                                  isMoreButton=False, flag='排行榜'))
        self.monthButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 5}', {'mode': 'month'}, title='月排行榜', isMoreButton=False,
                                  flag='排行榜'))
        self.weekButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 6}', {'mode': 'week'}, title='周排行榜', isMoreButton=False,
                                  flag='排行榜'))
        self.weekOriginalButton.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 7}', {'mode': 'week_original'}, title='周排行榜：原创',
                                  isMoreButton=False, flag='排行榜'))
        self.R18Button.clicked.connect(
            lambda: self.show_pic(f'illust_ranking{"+" * 8}', {'mode': 'day_r18'}, title='日R18', isMoreButton=False,
                                  flag='排行榜'))
        self.settingsButton.clicked.connect(self.Setting_page)
        # self.returnButton.clicked.connect(self.returnSmallPic)
        self.showDownloadButton.clicked.connect(self.show_download_detail)
        self.searchButton.clicked.connect(self.searchFrame.show_search_frame)
        self.aboutButton.clicked.connect(self.show_info)
        #self.cancelSearchButton.clicked.connect(self.hide_search_frame)
        self.infoFrame.escapeDownloadPageButton.clicked.connect(lambda: self.escapeDownloadPage(self.now_page))
        #self._searchButton.clicked.connect(lambda: self._search(isMoreButton=False))

    def _search(self, _mode={}, title="", isMoreButton=True):
        self.escapeDownloadPage(self.now_page)
        self.now_page = 'show_pic'
        self.returnSmallPic()
        self.searchFrame.hide_search_frame()
        if _mode == None:
            self.infoFrame.moreButton.setText('没有更多了')
            return
        word = self.searchFrame.searchLineEdit.text()
        print(word)
        if not word and not isMoreButton:  # 没有关键字又不是moreButton，是空关键字搜索，不允许
            self.searchFrame.searchLineEdit.setPlaceholderText("不允许空搜索")
            return
        elif isMoreButton:  # moreButton调用
            if word == 'None':
                self.infoFrame.moreButton.setText('没有更多了')
                return
            self.infoFrame.moreButton.setText('更多')
            word = _mode['word']
            sort = _mode['sort']
            duration = None
            _filter = _mode['filter']
            offset = _mode['offset']
            target = '画师'  # 当点击moreButton时，不会再调用_search，因此此变量可以直接赋值

        else:
            self.searchFrame.hide_search_frame()
            self.searchFrame.searchLineEdit.clear()
            sort = 'date_desc'
            duration = None
            _filter = 'for_ios'
            offset = None
            target = self.searchFrame.searchComboBox.currentText()

        title = f"{target}:{word}"
        print(title)
        if target == '标签':
            mode = {
                'word': word,
                'search_target': 'partial_match_for_tags',
                'sort': 'date_desc',
                'duration': None,
                'filter': 'for_ios',
                'offset': None
            }
            self.show_pic('', _mode=mode, title=title, isMoreButton=False, flag='标签作品')
        elif target == '画师':
            mode = {
                'word': word,
                'sort': sort,
                'duration': duration,
                'filter': _filter,
                'offset': offset
            }
            self.search_user(_mode=mode, title=f"{title}")

        elif target == '作品id':
            try:
                illust_id = int(word)
            except ValueError:
                print(f"int 不应该传入{word}")
                return
            mode = {
                'illust_id': illust_id
            }
            self.show_pic(_mode=mode, title=f"作品id：{illust_id}",isMoreButton=False, flag="作品id")

        elif target == '画师id':
            pass

    def add_key_to_result(self, ranking, info={}):
        illusts = [ranking['illust']]
        info['illusts'] = illusts
        info['next_url'] = None
        info['title'] = ranking['_title']
        return info

    def search_user(self, _mode, title, isSearch=True):
        from PyQt5.QtCore import QRect
        from Pixiv_Widget.My_Widget import my_widget

        if title not in self.tab:
            self.tab[title] = my_widget(flag='用户')
            self.tab[title].set_loading(False)
            ##self.tab[title].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            self.tab[title].setObjectName("tab[title]")
            
            # h = self.tabWidget.height()
            # w = self.tabWidget.width()
            # self.scrollAreas[title] = QScrollArea(self.tab[title])
            # self.scrollAreas[title].setGeometry(QRect(0, 0, w - 3, h - 32))
            # #self.scrollAreas[title].setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            # self.scrollAreas[title].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            # self.scrollAreas[title].setWidgetResizable(False)
            # self.scrollAreas[title].setObjectName("scrollArea")
            self.rebuild(title)
            self.tabWidget.addTab(self.tab[title], title)
            self.infoFrame.moreButton.disconnect()
            self.infoFrame.moreButton.clicked.connect(
                lambda: self.show_pic(self.method, self.next_url_s[title], title=title, flag='用户'))
            self.tab_title = title
            self.tabWidget.setCurrentIndex(len(self.tab) - 1)
            self.title_box.append(title)
            self.rank_pic_s[title] = 0
            self.threads = {}
            self.frames[title] = {}
            self.cache_item_box[title] = []

        if not self.cache_item_box[title]:
            if isSearch:
                word = _mode['word']
                sort = _mode.get('sort', 'date_desc')
                duration = _mode.get('duration', None)
                _filter = _mode.get('filter', 'for_ios')
                offset = _mode.get('offset', None)
                self.baseThread['search_user'] = base_thread(self, self.api.search_user,
                                                             info={'title': title},
                                                             word=word,
                                                             sort=sort,
                                                             duration=duration,
                                                             filter=_filter,
                                                             offset=offset)

            else:  # 点击左上角 我的...
                self.baseThread['search_user'] = eval(_mode['Thread'])

            self.baseThread['search_user'].finish.connect(self.show_user_info)
            self.baseThread['search_user'].wait()
            self.baseThread['search_user'].start()
        else:
            self.show_user_info({'title': title})

    def show_user_info(self, user_info):
        from Pixiv_Widget.Show_Users_Frame import show_users_frame

        title = user_info['title']  # tab_title
        self.scrollAreaWidgetContents[title].set_loading(False)

        if title not in self.cache_item_box:
            return

        elif not self.cache_item_box[title]:
            self.cache_item_box[title] = user_info['user_previews']
            self.next_url_s[title] = self.api.parse_qs(user_info['next_url'])

        self.infoFrame.moreButton.disconnect()
        self.infoFrame.moreButton.clicked.connect(lambda: self._search(self.next_url_s[title], title, isMoreButton=True))

        self.userIllustThread = {}
        self.userHeadThread = {}
        user_box = self.cache_item_box[title][:self.every_time_show_pic_num]
        n = 0
        for i in user_box:
            user_id = i['user']['id']
            info = {'user_preview': i, 'api': self.api, 'loading_gif': self.loading_gif,
                    'timeout_pic': self.timeout_pic, 'temp_path': self.temp_path, 'save_path': self.save_path,
                    'has_r18': self.has_r18, 'no_h': self.no_h, 'app': self}
            smallFrame_w = self.SmallFrame.width()
            scrollAreaWidgetContent_w = self.scrollAreaWidgetContents[title].width()
            frames_x = (scrollAreaWidgetContent_w - 790) // 2
            self.frames[title][user_id] = show_users_frame(self.scrollAreaWidgetContents[title], info=info)
            self.frames[title][user_id].setGeometry(QRect(frames_x, 370 * self.rank_pic_s[title], 790, 370))
            self.scrollAreaWidgetContents[title].resize(smallFrame_w - 20, 370 * (self.rank_pic_s[title] + 1))
            self.rank_pic_s[title] += 1

            self.frames[title][user_id].click.connect(self.show_big_pic)
            self.cache_item_box[title].pop(self.cache_item_box[title].index(i))
            n += 1

    def user_bookmarks_illust(self, user_id, restrict='public', _filter='for_ios', max_bookmark_id=None, tag=None):
        mode = {}
        mode['user_id'] = user_id
        mode['restrict'] = restrict
        mode['filter'] = _filter
        mode['max_bookmark_id'] = max_bookmark_id
        mode['tag'] = tag
        self.show_pic(f'user_bookmarks_illust-{mode["user_id"]}', _mode=mode, title='我的收藏', flag='收藏作品')

    def search_illust(self, word, search_target='partial_match_for_tags', sort='date_desc', duration=None,
                      _filter='for_ios', offset=None):
        # 标签点击调用
        word = word['tag']
        mode = {}
        mode['word'] = word
        mode['search_target'] = search_target
        mode['sort'] = sort
        mode['duration'] = duration
        mode['filter'] = _filter
        mode['offset'] = offset
        self.show_pic(f'search_illust-{mode["word"]}', _mode=mode, title=f"标签：{mode['word']}", flag='标签作品')

    def user_illusts(self, tag, _type='illust', _filter='for_ios', offset=None):
        # 点击左上角用户名，弹出Menu，其中'我的作品'调用
        user_id = tag['user_id']
        title = tag['title']
        mode = {}
        mode['user_id'] = int(user_id)
        mode['type'] = _type
        mode['filter'] = _filter
        mode['offset'] = offset
        self.show_pic(f'user_illusts-{mode["user_id"]}', _mode=mode, title=title, flag='用户作品')

    def escapeDownloadPage(self, now_page):
        self.table.setVisible(False)
        self.infoFrame.escapeDownloadPageButton.setVisible(False)
        self.infoFrame.moreButton.setVisible(True)
        self.DownloadPageScroll.setVisible(False)

        if now_page == 'show_pic':
            self.tabWidget.setVisible(True)
        elif now_page == 'show_big_pic':
            self.bigPicScrollArea.setVisible(True)
            self.comment_widget.setVisible(True)
            # self.bigReloadButton.setVisible(True)
            self.infoFrame.saveButton.setVisible(True)
            self.infoFrame.authText.setVisible(True)
            self.infoFrame.titleText.setVisible(True)
            self.infoFrame.text_scroll.setVisible(True)
            self.infoFrame.user_pic_label.setVisible(True)

    def _logout(self):
        from Pixiv_Widget.Pixiv_Login import app_logout
        def del_p():
            del self.p

        if hasattr(self, 'p'):
            self.p.show()
            return True
        self.p = app_logout(self, main=main)
        self.p.closed.connect(del_p)
        self.p.show()
        return True

    def closeEvent(self, event):
        # 待解决,关闭后删除某些东西
        log_file_list = os.listdir('log_file')
        for file in log_file_list:
            _file = f'log_file/{file}'
            if not os.path.getsize(_file):
                os.remove(_file)

    #@profile
    def show_big_pic(self, info):
        from PyQt5.QtWidgets import QWidget
        from PyQt5 import sip
        from Pixiv_Widget.Big_Pic_Frame import big_pic_frame

        illust = info['illust']

        illust_id = illust['id']
        tags = illust['tags']

        self.now_page = 'show_big_pic'
        # 点击“大图”按钮后小图列表不可见，大图列表可见
        self.big_pic = 0  # 该illust的图片数目
        self.infoFrame.user_pic_label.setVisible(True)
        self.infoFrame.saveButton.setVisible(True)
        self.infoFrame.authText.setVisible(True)
        self.infoFrame.titleText.setVisible(True)
        self.infoFrame.text_scroll.setVisible(True)
        self.bigPicScrollArea.setVisible(True)
        if hasattr(self, 'comment_widget'):
            self.comment_widget.setVisible(True)
        self.tabWidget.setVisible(False)

        ### 销毁QWidget
        child_widget = self.scrollAreaWidgetContents_3.findChild(big_pic_frame)
        if not child_widget:
            big_pic_frame_illust_id = -1
        else:
            big_pic_frame_illust_id = child_widget.info['illust_id']

        if int(illust_id) != int(big_pic_frame_illust_id):
            for i in self.scrollAreaWidgetContents_3.children():
                i.deleteLater()
                sip.delete(i)

            self.scrollAreaWidgetContents_3.deleteLater()
            sip.delete(self.scrollAreaWidgetContents_3)
            ###
            ### 重建scrollArea里的QWidget
            self.scrollAreaWidgetContents_3 = Scroll_Widget()
            self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
            self.bigPicScrollArea.setWidget(self.scrollAreaWidgetContents_3)

        # del self.threads
        # self.threads = {}

        # del self.bigFrames
        # self.bigFrames = {}

        info = {"illust": illust, "api": self.api}
        self.infoFrame.create_illust_detail_panel(info=info)

        n = 1
        if illust['meta_single_page']:
            file_name = f"{illust_id}_{n}"

            self.create_big_pic_panel(url=illust['image_urls'][self.big_pic_size],
                                      original_url=illust['meta_single_page']['original_image_url'],
                                      file_name=file_name, title=f"{illust['title']}", tags=tags, illust_id=illust_id)

        else:
            for j in illust['meta_pages']:
                file_name = f"{illust_id}_{n}"
                self.create_big_pic_panel(url=j['image_urls'][self.big_pic_size],
                                          original_url=j['image_urls']['original'], file_name=file_name,
                                          title=f"{illust['title']}_{n}p", tags=tags, illust_id=illust_id)
                n += 1
        # 为了滑到最底时有空白
        w = self.scrollAreaWidgetContents_3.width()
        h = self.scrollAreaWidgetContents_3.height()
        self.scrollAreaWidgetContents_3.resize(w, h + 10)
        ###

        # 重建并加载评论区
        try:
            self.comment_widget.deleteLater()
            sip.delete(self.comment_widget)

        except:
            pass
        self.comment_widget = Comment_Widget(self.SmallFrame, info={'api': self.api, 'illust': illust_id, 'temp_path': self.temp_path})
        self.comment_widget.move(self.bigPicScrollArea.x() + self.bigPicScrollArea.width(), self.bigPicScrollArea.y())
        self.comment_widget.resize(self.comment_widget.width(), self.bigPicScrollArea.height())
        self.comment_widget.show()
        self.infoFrame.raise_()

        # 创建作品相关区
        info = {'api': self.api, 'illust_id': illust['id'], 'temp_path': self.temp_path, 'has_r18': self.has_r18, 'no_h': self.no_h}
        self.illust_related_frame = Illust_Relate(self.scrollAreaWidgetContents_3, info=info)
        smallFrame_w = self.SmallFrame.width()
        illust_related_frame_w = self.illust_related_frame.width()
        self.illust_related_frame.move(
            (smallFrame_w - 360 - 644) // 2, self.scrollAreaWidgetContents_3.height())  # 644是illust_related_frame的宽度(本是620， 增加24是为了相关图放大后可以完全显示)， 360 评论区宽度， smallFrame-360 是 self.scrollAreaWidgetContents_3的宽度
        self.scrollAreaWidgetContents_3.resize(smallFrame_w - 360, self.scrollAreaWidgetContents_3.height() + 744 + 24) # 为相关图放大后可以完全显示而加上24（计算好的结果）
        self.illust_related_frame.one_label_is_clicked.connect(self.show_big_pic)
        #self.illust_related_frame.setStyleSheet('background-color: rgb(231, 195, 188)')
        self.illust_related_frame.show()
        ###


    #@profile
    def load_user_head(self, info):
        # 加载用户头像
        label = self.login_user_pic_label
        url = info['url']
        file_name = info['file_name']

        if info['isSuccess']:
            file = f"{self.temp_path}/{file_name}"
        else:
            file = self.timeout_pic
        print(file)
        try:
            picture = QPixmap(file).scaled(label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            if picture.isNull():
                try:
                    os.remove(file)
                except:
                    pass
                self.baseThread[file_name] = base_thread(self, self.api.cache_pic, url=url, path=self.temp_path,
                                                         file_name=file_name,
                                                         info={'file_name': file_name, 'url': url, 'row': 1062})
                self.baseThread[file_name].finish.connect(self.load_user_head)
                self.baseThread[file_name].wait()
                self.baseThread[file_name].start()
                return
            label.setPixmap(picture)
        except (RuntimeError, KeyError, PermissionError) as e:
            pass

    def simulateSearch(self, word):
        print(word)
        currentText = self.searchFrame.searchComboBox.currentText()
        self.searchFrame.searchLineEdit.setText(word['tag'])
        self.searchFrame.searchComboBox.setCurrentText('画师')
        self._search(isMoreButton=False)
        self.searchFrame.searchComboBox.setCurrentText(currentText)

    #@profile
    def create_big_pic_panel(self, url, original_url, file_name, title, tags, illust_id):
        from Pixiv_Widget.Big_Pic_Frame import big_pic_frame

        info = {
            'api': self.api,
            'url': url,
            'temp_path': self.temp_path,
            'temp_file_name': file_name,
            'title': title,
            'timeout_pic': self.timeout_pic,
            'original_pic_url': original_url,
            'tags': tags,
            'illust_id': illust_id
        }

        self.bigFrames[file_name] = big_pic_frame(self.scrollAreaWidgetContents_3, info=info)
        self.bigFrames[file_name].image_load_completly.connect(self.scrollAreaWidgetContents_3.adjust_size)

        self.bigFrames[file_name].double_click.connect(self.show_original_pic)

        self.bigFrames[file_name].show()
        smallFrame_w = self.SmallFrame.width()
        self.bigFrames[file_name].move(
            (smallFrame_w - 360 - 620) // 2, self.scrollAreaWidgetContents_3.height())
        self.scrollAreaWidgetContents_3.resize(smallFrame_w - 360, self.bigFrames[file_name].height() + self.scrollAreaWidgetContents_3.height() + 5)
    
        self.big_pic += 1

    def show_original_pic(self, info):
        def try_pop(url):
            try:
                self.sub_windows.pop(url)
            except:
                pass

        url = info['original_pic_url']
        title = info['title']
        file_name = info['temp_file_name']  # 已加后缀_original
        temp_path = info['temp_path']

        if url in self.sub_windows:
            return
        info = {
            'url': url,
            'temp_path': temp_path,
            'temp_file_name': file_name,
            'api': self.api,
            'loading_gif': self.loading_gif,
            'title': title,
            'timeout_pic': self.timeout_pic,
        }
        self.sub_windows[url] = original_pic(parent=self, info=info)
        self.sub_windows[url].myclosed.connect(lambda: try_pop(url))
        self.sub_windows[url].setWindowTitle(title)

    def saveOriginalPic(self, illust):
        import re
        self.getImageSizeThreads = {}
        illust_id = illust['id']
        title = illust['title']
        titlePath = re.sub(r'[?/\*<>:|]', '_', title)
        file_name = re.sub(r'[?/\*<>:|]', '_', title)
        n = 1
        if illust['meta_single_page']:
            self.getImageSizeThreads[f"{illust_id}_{n}"] = base_thread(self, self.api.get_image_size,
                                                                       url=illust['meta_single_page'][
                                                                           'original_image_url'],
                                                                       info={'n': n, 'illust_id': illust_id,
                                                                             'url': illust['meta_single_page'][
                                                                                 'original_image_url'], 'title': title})
            self.getImageSizeThreads[f"{illust_id}_{n}"].finish.connect(self.download_or_not)
            self.getImageSizeThreads[f"{illust_id}_{n}"].wait()
            self.getImageSizeThreads[f"{illust_id}_{n}"].start()

            file = f"{self.save_path}/{titlePath}_{illust_id}/{file_name}_{n}.jpg"
            info = {'image_size': None, 'save_file': file, 'download_timer_id': f"{illust_id}_{n}", "n": n}
            self.create_download_progress(info=info)

        for j in illust['meta_pages']:
            self.getImageSizeThreads[f"{illust_id}_{n}"] = base_thread(self, self.api.get_image_size,
                                                                       url=j['image_urls']['original'],
                                                                       info={'n': n, 'illust_id': illust_id,
                                                                             'url': j['image_urls']['original'],
                                                                             'title': title})
            self.getImageSizeThreads[f"{illust_id}_{n}"].finish.connect(self.download_or_not)
            self.getImageSizeThreads[f"{illust_id}_{n}"].wait()
            self.getImageSizeThreads[f"{illust_id}_{n}"].start()
            
            file = f"{self.save_path}/{titlePath}_{illust_id}/{file_name}_{n}.jpg"
            info = {'image_size': None, 'save_file': file, 'download_timer_id': f"{illust_id}_{n}", "n": n}
            self.create_download_progress(info=info)

            n += 1

        if not self.table.isVisible():
            self.downloadTipsLabel.setVisible(True)

    def download_or_not(self, result):
        import re
        import os
        import shutil

        image_size = int(result['image_size'])
        n = result['n']
        illust_id = result['illust_id']
        url = result['url']
        title = result['title']

        temp_file_name = f"{illust_id}_{n}_original"

        dontDownload = 0
        titlePath = re.sub(r'[?/\*<>:|]', '_', title)
        file_name = re.sub(r'[?/\*<>:|]', '_', title)
        try:
            os.mkdir(f'{self.save_path}/{titlePath}_{illust_id}')
        except:
            pass
        tempFile = f"{self.temp_path}/{temp_file_name}"
        file = f"{self.save_path}/{titlePath}_{illust_id}/{file_name}_{n}.jpg"
        path = f"{self.save_path}/{titlePath}_{illust_id}"
        if not self.remove_imperfect_image(file, image_size):
            print('You have the same.')
            dontDownload = 1
        elif not self.remove_imperfect_image(tempFile, image_size):
            try:
                shutil.copyfile(tempFile, file)
            except Exception as e:
                print(e, 'e' * 90)
            else:
                dontDownload = 1

        info = {'image_size': int(image_size), 'save_file': file, 'download_timer_id': f"{illust_id}_{n}", 'n': n}
        self.create_download_progress(info=info)

        if not dontDownload:
            self.downloadThreads[f"{illust_id}_{n}"] = base_thread(self, self.api.download, url=url, path=path,
                                                                   name=f"{file_name}_{n}.jpg")
            self.downloadThreads[f"{illust_id}_{n}"].start()

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

    def show_download_detail(self):
        if self.infoFrame.detail_is_show():
            self.infoFrame.hide_illust_detail()
        self.infoFrame.saveButton.setVisible(False)
        self.infoFrame.titleText.setVisible(False)
        self.infoFrame.authText.setVisible(False)
        self.infoFrame.text_scroll.setVisible(False)
        self.bigPicScrollArea.setVisible(False)
        self.infoFrame.user_pic_label.setVisible(False)
        if hasattr(self, 'comment_widget'):
            self.comment_widget.setVisible(False)
        # self.bigReloadButton.setVisible(False)
        # self.table.setVisible(False)
        # self.infoFrame.escapeDownloadPageButton.setVisible(False)
        self.tabWidget.setVisible(False)
        self.infoFrame.moreButton.setVisible(False)

        self.table.setVisible(True)
        self.infoFrame.escapeDownloadPageButton.setVisible(True)
        self.downloadTipsLabel.setVisible(False)

    def create_download_progress(self, info):
        from PyQt5.QtGui import QStandardItem
        from PyQt5.QtGui import QBrush
        from PyQt5.QtGui import QColor
        from PyQt5.QtCore import QTimer

        image_size = info['image_size']
        file = info['save_file']
        d_timer_id = info['download_timer_id']
        n = info['n'] - 1   # 一个作品的第n张图片

        row = self.table.model().rowCount()

        file_name = file.split('/')[-1][:-4]
        if image_size is None:
            self.table._model.setItem(row, 0, QStandardItem(file_name))
            self.table._model.setItem(row, 1, QStandardItem('等待下载'))
            self.table._model.setItem(row, 2, QStandardItem('0%'))
            self.table._model.item(row, 0).setForeground(QBrush(QColor(255, 255, 255)))
            self.table._model.item(row, 1).setForeground(QBrush(QColor(255, 255, 255)))
            self.table._model.item(row, 2).setForeground(QBrush(QColor(255, 255, 255)))

            self.table.info[d_timer_id] = row

        if not image_size is None:
            self.downloadTimer[d_timer_id] = QTimer()
            self.downloadTimer[d_timer_id].timeout.connect(
                lambda: self.table.count_process(image_size, file, self.downloadTimer[d_timer_id], d_timer_id, file_name))
            self.downloadTimer[d_timer_id].start(1000)

        #self.downloadNum += 1

    # @profile
    def returnSmallPic(self):
        if self.infoFrame.detail_is_show():  # 复原详情
            self.infoFrame.hide_illust_detail()

        del self.bigFrames
        self.bigFrames = {}
        self.infoFrame.saveButton.setVisible(False)
        self.infoFrame.authText.setVisible(False)
        self.infoFrame.titleText.setVisible(False)
        self.infoFrame.text_scroll.setVisible(False)
        self.bigPicScrollArea.setVisible(False)
        if hasattr(self, 'comment_widget'):
            self.comment_widget.setVisible(False)
        self.infoFrame.user_pic_label.setVisible(False)
        # self.bigReloadButton.setVisible(False)
        self.table.setVisible(False)
        self.infoFrame.escapeDownloadPageButton.setVisible(False)
        self.tabWidget.setVisible(True)
        self.infoFrame.moreButton.setText('更多')
        try:
            self.infoFrame.moreButton.disconnect()
        except TypeError:
            pass
        index = self.tabWidget.currentIndex()
        title = self.tabWidget.tabText(index)
        try:
            flag = self.tab[title].flag
        except:
            flag = ''
        self.now_page = 'show_pic'
        if flag != '用户':
            self.infoFrame.moreButton.clicked.connect(
                lambda: self.show_pic(self.method, self.next_url_s[title], title, flag=flag))
        else:
            self.infoFrame.moreButton.clicked.connect(lambda: self._search(self.next_url_s[title], title))


    def resizeEvent(self, event=None):
        height = self.height()  # 原始809
        width = self.width()

        # self.resize(event.oldSize().width(), height)

        # 修改左侧按钮
        frame_h = self.frame.height()
        cate_scrollArea_w = self.cate_scrollArea.width()
        function_frame_h = self.function_frame.height()
        cate_scrollArea_new_h = height - function_frame_h - frame_h
        function_frame_y = height - function_frame_h
        function_frame_x = self.function_frame.x()
        self.function_frame.move(function_frame_x, function_frame_y)
        self.cate_scrollArea.resize(cate_scrollArea_w, cate_scrollArea_new_h)

        ###

        # 修改右侧控件尺寸及按钮位置
        # smallFrame_width = width #self.SmallFrame.width()
        self.SmallFrame.resize(width - 117, height)

        smallFrame_w = self.SmallFrame.width()
        smallFrame_h = self.SmallFrame.height()

        # downloadPageScroll_width = self.SmallFrame.width() #self.table.width()
        infoFrame_h = self.infoFrame.height()
        self.table.resize(smallFrame_w, height - infoFrame_h)

        self.bigPicScrollArea.resize(smallFrame_w-340, height - 80)
        self.scrollAreaWidgetContents_3.resize(smallFrame_w - 360, self.scrollAreaWidgetContents_3.height())
        for i in self.scrollAreaWidgetContents_3.children():
            bigFrame_x = (self.scrollAreaWidgetContents_3.width() - i.width()) // 2
            y = i.y()
            i.move(bigFrame_x, y)


        # 调整评论区
        if hasattr(self, 'comment_widget'):
            self.comment_widget.move(self.bigPicScrollArea.x() + self.bigPicScrollArea.width(), self.bigPicScrollArea.y())
            self.comment_widget.resize(self.comment_widget.width(), self.bigPicScrollArea.height())

        # self.scrollAreaWidgetContents_3.setStyleSheet("background-color: black")

        self.tabWidget.resize(smallFrame_w, height - infoFrame_h)

        for i in self.tab:
            self.tab[i].resize(smallFrame_w, height - 107)
            self.scrollAreas[i].resize(smallFrame_w - 3, height - 105)

        per_row_should_pic_num = (smallFrame_w - 18) // 240  # 计算每行最多可显示多少张图(一张图占宽240)

        if per_row_should_pic_num != self.now_per_row_pic_num and per_row_should_pic_num >= 1:
            x = {0: 0, 1: 240, 2: 480, 3: 720, 4: 960, 5: 1200, 6: 1440, 7: 1680, 8: 1920, 9: 2160}
            self.now_per_row_pic_num = per_row_should_pic_num
            for title in self.frames:
                flag = self.tab[title].flag
                if flag == '用户':
                    continue
                else:
                    n = 0
                    for i in self.frames[title]:
                        try:
                            self.frames[title][i].move(x[n % self.now_per_row_pic_num],
                                                       ((n // self.now_per_row_pic_num)) * 411)
                        except KeyError:
                            pass
                        n += 1
        for i in self.scrollAreaWidgetContents:
            flag = self.tab[i].flag
            if flag == '用户':
                scrollAreaWidgetContent_h = self.scrollAreaWidgetContents[i].height()
                self.scrollAreaWidgetContents[i].resize(smallFrame_w - 20, scrollAreaWidgetContent_h)
                child_list = self.scrollAreaWidgetContents[i].children()
                scrollAreaWidgetContents_w = self.scrollAreaWidgetContents[i].width()
                for child in child_list:
                    child_w = child.width()
                    child_y = child.y()
                    child_new_x = int((scrollAreaWidgetContents_w - child_w) / 2)
                    child.move(child_new_x, child_y)
            else:
                self.scrollAreaWidgetContents[i].resize(self.now_per_row_pic_num * 240,
                                                        (ceil((self.rank_pic_s[i]) / self.now_per_row_pic_num)) * 411)
        # self.scrollAreaWidgetContents_2.setStyleSheet("background-color: black")

        # 调整搜索框
        searchFrame_x = self.searchFrame.x()
        searchFrame_y = self.searchFrame.y()
        searchFrame_h = self.searchFrame.height()
        self.searchFrame.setGeometry(QRect(searchFrame_x, searchFrame_y, smallFrame_w, searchFrame_h))

        ###

        # 调整下方详情frame
        info_x = self.infoFrame.x()
        info_h = self.infoFrame.height()
        self.infoFrame.setGeometry(QRect(info_x, height - info_h, smallFrame_w, info_h))

    def keyPressEvent(self, qevent):
        if qevent.key() == 16777216: # Esc
            self.searchFrame.hide_search_frame()
        elif qevent.key() == 16777220:    # Enter
            self._search(isMoreButton=False)
            self.searchFrame.show_search_frame()

        elif qevent.key() == Qt.Key_F:
            self.test()

        elif qevent.key() == Qt.Key_S:
            self.set_style()

    def set_style(self):
        f = open('Main_Style.qss', encoding='utf-8')
        style = f.read()
        self.setStyleSheet(style)
        f.close()
        self.update()

    def Setting_page(self):
        info = {}
        info['big_pic_size'] = self.big_pic_size
        info['per_row_pic_num'] = self.per_row_pic_num
        info['temp_path'] = self.temp_path
        info['save_path'] = self.save_path
        info['has_r18'] = self.has_r18
        info['every_time_show_pic_num'] = self.every_time_show_pic_num

        self.setting_window = setting_window(self, info=info)
        self.setting_window.setWindowTitle("设置")
        self.setting_window._closed.connect(self.set_user_setting)
        self.setting_window.show()

    def set_user_setting(self, _setting):
        from utils.Project_Setting import setting
        cfg = setting()
        cfg.set_user_setting(_setting)
        self.get_setting()
        self.R18Button.setVisible(self.has_r18)
        self.ajust_cate_widget_size()

    def test(self, info=None):
        return 
        from find import IKnowChildren
        print('开始写入！')
        import time
        p = int(time.time())
        k = str(p)[-3:]
        f = open(f'Widget_Children-{k}.csv', 'w', encoding='utf-8')
        f.write('层级@序号@对象名@类别@内存@x@y@w@h@style_sheet@子对象名@子类别@子内存@_x@_y@_w@_h@sub_style_sheet\n')
        f.close()
        a = IKnowChildren()
        for i in a.find_children(self):
            f = open(f'Widget_Children-{k}.csv', 'a', encoding='utf-8')
            print(i, end='')
            f.write(i)
            f.close()
        print('手工！')
        import pandas as pd
        
        n = pd.read_csv(f'Widget_Children-{k}.csv', sep='@')
        n.to_excel(f'Widget_Children-{k}.xlsx', index=0)

def login_success(login, user_id, username, user_pic_link):
    global AppUi
    AppUi = main_pixiv(login.api, user_id, username, user_pic_link)
    # AppUi.showMinimized()
    login.close()
    del (login)


def main():
    global login
    try:
        del (AppUi)
    except:
        pass
    login = app_login(login_success)
    # login.move(2000, 1000)
    # login.showMinimized()
    login.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main()
    sys.exit(app.exec_())
