#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
import time
import os


import cgitb
cgitb.enable(format='text', logdir='log_file')
class TableView(QtWidgets.QTableView):
    def __init__(self, parent, *args, **kwargs):
        super(TableView, self).__init__(parent, *args, **kwargs)
        self.info = {}

    def setupUi(self):
        self._model = QtGui.QStandardItemModel(0, 3)
        self._model.setHorizontalHeaderLabels(['文件', '下载状态', '进度'])
        self.setModel(self._model)
        #self.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgba(0, 0, 0, 0);font:13pt '宋体';color: white;};")
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def count_process(self, image_size, file, timer, d_timer_id, file_name):
        row = self.info[d_timer_id]
        print(f"row = {row}")
        value = 0
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            value = int((file_size/image_size)*100)
            download_status = "下载中"
        else:
            download_status = "等待下载"
        self._model.setItem(row, 2, QtGui.QStandardItem(f"{value}%"))
        self._model.setItem(row, 1, QtGui.QStandardItem(download_status))
        
        if value >= 100:
            self._model.setItem(row, 1, QtGui.QStandardItem("下载完成"))
            timer.stop()
        self._model.item(row, 1).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self._model.item(row, 2).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))

    def set_download_failure(self, info):
        isSuccess = info['isSuccess']
        timer_box = info['timer_box']
        d_timer_id = info['download_timer_id']
        row = self.info[d_timer_id]
        if not isSuccess:
            timer_box[d_timer_id].stop()
            self._model.setItem(row, 1, QtGui.QStandardItem("下载失败"))
            self._model.item(row, 1).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        
 
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    qb = ProgressBar()
    qb.show()
    sys.exit(app.exec_())
