
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import pixivpy3
import time


import cgitb
cgitb.enable(format='text', logdir='log_file')

class QMutex_Manager:
    thread_pool = 10     # 线程限制在thread_pool个
    wait_mutex = 0      # 当没有闲置锁时，在第wait_mutex个锁等待
    mutex_status = {i: True for i in range(thread_pool)}
    mutex_box = {i: QMutex() for i in range(thread_pool)}

    @classmethod
    def get_mutex(cls, *args, **kwargs):
        for i in cls.mutex_status:
            if cls.mutex_status[i]:
                return i

        # 没有闲置锁，在第i个等待
        i = cls.wait_mutex
        cls.wait_mutex += 1
        if cls.wait_mutex >= cls.thread_pool:
            cls.wait_mutex = 0
        return i


class base_thread(QThread):
    # 除更新UI以外的其他操作
    """docstring for DownloadThread"""
    finish = pyqtSignal(dict)
    none_finish = pyqtSignal()
    thread_pool = 5     # 特定线程限制在thread_pool个
    root = None

    def __init__(self, parent, method, info={}, **args):
        super(base_thread, self).__init__(self.root)
        self.method = method
        self.args = args
        self.info = info

    #@profile
    def run(self):
        lock_id = QMutex_Manager.get_mutex()
        QMutex_Manager.mutex_box[lock_id].lock()
        QMutex_Manager.mutex_status[lock_id] = False
        try:
            a = self.method(**self.args)
        except pixivpy3.utils.PixivError:
            error_info = {'info': self.info}    # 传递给连接好的函数
            error_info.update({'ERROR': True})  
            error_info.update({'method': self.method, 'args': self.args})   # 提供网络错误时执行的函数及该函数所需的参数
            self.finish.emit(error_info)
        else:
            if isinstance(a, dict):
                a.update(self.info)
                self.finish.emit(a)
            else:
                self.none_finish.emit()

        QMutex_Manager.mutex_box[lock_id].unlock()
        QMutex_Manager.mutex_status[lock_id] = True


if __name__ == '__main__':
    import sys
    import time

    from PyQt5.QtWidgets import QFrame, QApplication, QPushButton

    class myq(QFrame):
        index = 0

        def count(self, index):
            for i in range(3):
                print(index)
                time.sleep(1)

            return {'index': index}

        def start_thread(self):
            self.index += 1
            p = lambda x: print(x)
            base_thread.root = self
            n = base_thread(self, self.count, index=self.index, info={'index': self.index})
            n.finish.connect(lambda x: print(f"{x['index']} done"))
            n.wait()
            n.start()

    app = QApplication(sys.argv)
    a = myq()
    b = QPushButton(a)
    b.clicked.connect(a.start_thread)
    b.resize(50, 25)
    b.move(25, 12)
    b.setText('000')
    a.resize(100, 50)
    a.move(2000, 1000)
    a.show()
    sys.exit(app.exec_())

