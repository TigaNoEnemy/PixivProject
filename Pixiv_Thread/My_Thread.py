#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import pyqtSignal, QObject
from concurrent.futures import ThreadPoolExecutor
import pixivpy3
import time


import cgitb
cgitb.enable(format='text', logdir='log_file')


THREAD_POOL = ThreadPoolExecutor(max_workers=10)

class base_thread(QObject):
    # 除更新UI以外的其他操作
    """docstring for DownloadThread"""
    finish = pyqtSignal(dict)
    root = None

    def __init__(self, parent, method, info={}, **args):
        super(base_thread, self).__init__(self.root)
        self.method = method
        self.args = args
        self.info = info

    def start(self):
        future = THREAD_POOL.submit(self.method, **self.args)
        future.add_done_callback(self.emit_signal)

    def emit_signal(self, future):
        result = future.result()
        result.update(self.info)
        result.update(self.args)
        self.finish.emit(result)

    def wait(self):
        pass


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

