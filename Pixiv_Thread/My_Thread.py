#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import pixivpy3
import time
from memory_profiler import profile


import cgitb
cgitb.enable(format='text', logdir='log_file')
class small_frame_thread_num:
    # 指示当前有多少个预览图下载线程
    num = 0

class big_frame_thread_num:
    # 指示当前有多少个大图下载线程
    num = 0

class base_thread(QThread):
    # 除更新UI以外的其他操作
    """docstring for DownloadThread"""
    finish = pyqtSignal(dict)
    none_finish = pyqtSignal()
    thread_pool = 5     # 特定线程限制在thread_pool个

    def __init__(self, parent, method, info={}, **argv):
        super(base_thread, self).__init__()
        self.method = method
        print(self.method, '**********************')
        self.argv = argv
        self.info = info
        self.parent = parent

    #@profile
    def run(self):
        frame = self.info.get('self', None)

        if frame == 'small':
            while small_frame_thread_num.num >= self.thread_pool:
                time.sleep(1)
            small_frame_thread_num.num += 1

        elif frame == 'big':
            while big_frame_thread_num.num >= self.thread_pool:
                time.sleep(1)
            big_frame_thread_num.num += 1

        command = f'self.method('
        for i in self.argv:
            if isinstance(self.argv[i], str):
                command += f'{i}="{self.argv[i]}",'
            else:
                command += f'{i}={self.argv[i]},'
        if command.endswith(','):
            command = command[:-1]
        command += ')'
        try:
            a = eval(command)
        except pixivpy3.utils.PixivError:
            self.finish.emit({'ERROR': True})
        else:
            if isinstance(a, dict):
                a.update(self.info)
                self.finish.emit(a)
            else:
                self.none_finish.emit()

        if frame == 'small':
            small_frame_thread_num.num -= 1

        elif frame == 'big':
            big_frame_thread_num.num -= 1

        #del self