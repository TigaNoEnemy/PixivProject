#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from configparser import ConfigParser
import configparser
import sys

import cgitb
cgitb.enable(format='text', logdir='log_file')

class setting(ConfigParser):
    _instance = None

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(setting, self).__init__()
        if sys.platform == 'linux':
            self.setting_file = 'settings.cfg'
            self.wrap_split = '\n'
        else:
            self.setting_file = 'settings.ini'
            self.wrap_split = '\r'
        try:
            self.get_setting()
        except:
            self.set_settings_default()
            self.get_setting()

    def get_setting(self):
        # 获取配置信息 
        self.read(self.setting_file, encoding='utf-8')
        self.temp_path = self.get('RES', 'temp_path').replace('\\', '/')
        self.save_path = self.get('RES', 'save_path').replace('\\', '/')

        self.big_pic_size = self.get('RES', 'big_pic_size') # small, medium, large
        self.timeout_pic = self.get('RES', 'timeout_pic')   # 加载超时时显示的图片
        # self.loading_gif = self.get('RES', 'loading_gif') # 加载预览图时显示的GIF动画
        # self.login_background = self.get('RES', 'login_background') # 登录界面的背景
        # self.main_window_background = self.get('RES', 'main_window_background') # 程序主界面背景
        # self.font_color = self.get('RES', 'font_color') # 字体颜色
        # self.font = self.get('RES', 'font') # 字体
        # self.press_color = self.get('RES', 'press_color') # 点击按钮背景颜色
        # self.focus_color = self.get('RES', 'focus_color') # 光标悬浮于按钮时，显示按钮的颜色
        self.app_icon = self.get('RES', 'app_icon') # 应用图标
        # self.loading_big_gif = self.get('RES', 'loading_big_gif') # 加载大图时的GIF
        self.login_gif = self.get('RES', 'login_gif') # 登录时显示的GIF
        self.has_r18 = eval(self.get('RES', 'has_r18')) # 是否显示R18图片
        every_time_show_pic_num = int(self.get('RES', 'every_time_show_pic_num'))  
        if every_time_show_pic_num >= 30:
            every_time_show_pic_num = 30
        elif every_time_show_pic_num <= 1:
            every_time_show_pic_num = 1
        self.every_time_show_pic_num = every_time_show_pic_num  # 每次点击最多显示多少张图片（仅适用于预览图片）
        self.tips_dot = self.get('RES', 'tips_dot')  # 新增下载时显示的图片
        per_row_pic_num = int(float(self.get('RES', 'per_row_pic_num')))
        if per_row_pic_num <= 0:
            per_row_pic_num = 1
        elif per_row_pic_num >= 7:
            per_row_pic_num = 7
        self.per_row_pic_num = per_row_pic_num  # 预览图片时一行多少张
        self.timeout = float(self.get('RES', 'timeout')) # 网络请求的超时时间
        self.no_h = self.get('RES', 'no_h') # 禁止显示r18图片时，代替r18图片的图片

    # 设置配置信息
    def set_user_setting(self, _setting):
        self.read(self.setting_file, encoding='utf-8')
        for k, v in _setting.items():
            v = str(v).replace('\\', '/')
            self.set('RES', k, str(v))
        self.write(open(self.setting_file, 'w', encoding='utf-8'))

    #重置配置信息
    def set_settings_default(self):
        import os

        work_dir = os.getcwd()
        temp_path = f"{work_dir}/pixivTmp"
        save_path = f"{work_dir}/Pixiv"

        # 重置配置
        default = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PixivProject settings

# 注意！注意！注意！修改本文件有可能导致文件无法运行！

[RES]
# 一行图片数
per_row_pic_num = 4

# 资源文件夹
RESOURCE = ./RES

# 缓存文件夹
temp_path = {temp_path}

# 保存文件夹
save_path = {save_path}
# 查看大图时，加载图片的尺寸：square_medium, medium, large
big_pic_size = large 

AUTOFILE = ./RES/.auto

tips_dot = ./RES/DOWNLOAD_TIPS.png

# 加载图片失败时，默认加载的图片
timeout_pic = ./RES/timeout_pic

# 加载图片时显示的动图(已废弃)
# loading_gif = ./RES/loading_small.gif

# 登录界面背景，界面窗口大小为: 1158x809(已废弃)
# login_background = ./RES/background.jpg

# 浏览界面背景，界面窗口大小为: 1158x809(已废弃)
# main_window_background = ./RES/background.jpg

# 部分文字颜色(已废弃)
# font_color = rgb(255, 255, 255);
# focus_color = lightblue
# press_color = black

# 部分文字字体(已废弃)
# font = 12pt "Noto Sans CJK SC";

# 软件图标
app_icon = ./RES/pixiv.ico

# 加载大图时显示的动图(已废弃)
# loading_big_gif = ./RES/loading_large.gif

# 每次操作只加载最多多少张图(可设置的最大数应小于等于Pixiv接口的返回数， 若大于其返回数则不会生效)
# 该设置不适用于大图浏览
every_time_show_pic_num = 20


# 登录动图
login_gif = ./RES/login_gif

has_r18 = False

# 加载图片的超时时间
timeout = 5
no_h = ./RES/no_h'''.replace('\n', self.wrap_split)

        f = open(self.setting_file, 'w', encoding='utf-8')
        f.write(default)
        f.close()

    # 验证文件是否存在并是否创建
    def check_file(self):
        import os
        if not os.path.exists(self.temp_path):
            os.mkdir(self.temp_path)
        if not os.path.exists(self.save_path):
            os.mkdir(self.save_path)
        if not os.path.exists('log_file'):
            os.mkdir('log_file')
        print('Complete: check_file')
        return {'isSucess': True}

def print_setting(cfg):
    f = open(cfg.setting_file)
    a = f.read()
    print(a)
    f.close()

if __name__ == '__main__':
    cfg = setting()
    cfg.set_settings_default()
    print_setting(cfg)
    #cfg.set_user_setting(_setting={'temp_path': '/home/k', 'save_path': '/home/j'})
    print_setting(cfg)
    print(dir(cfg))