#!/usr/bin/env python3
from PyQt5.QtGui import QStandardItem, QBrush, QColor, QStandardItemModel
from PyQt5.QtWidgets import QTableView, QHeaderView, QAbstractItemView, QHBoxLayout, QItemDelegate, QPushButton, QWidget
from PyQt5.QtCore import QTimer, Qt
import time
import os


import cgitb
cgitb.enable(format='text', logdir='log_file')

class My_Item(QStandardItem):
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info', {})
        super().__init__(*args, **kwargs)
        
class Operate_Button(QItemDelegate):
    """docstring for Operate_Button"""
    def __init__(self, parent=None, info={}):
        super(Operate_Button, self).__init__(parent)

    def button_callback(self, index):
        import platform
        file = index.model().item(index.row(), 0).info['file']
        
        file_dir = file.split('/')[:-1]
        file_dir = '/'.join(file_dir)

        if platform.system() == "Windows":
            import os
            os.startfile(file_dir)
        else:
            import subprocess
            subprocess.call(['xdg-open', file_dir])

    def reconnect(self, index):
        item = index.model().item(index.row(), 0)
        timer_box = item.info['timer_box']
        d_timer_id = item.info['d_timer_id']
        if timer_box[d_timer_id].isActive():
            return
        
        root = item.info['main']
        root.getImageSizeThreads[d_timer_id].start()

        # image_size = item.info['image_size']
        file = item.info['file']
        
        # d_timer_id = item.info['d_timer_id']
        # file_name = item.info['file_name']
        row = item.info['row']

        info = item.info.copy()
        info['save_file'] = file
        info['download_timer_id'] = d_timer_id
        # self.parent()._model.removeRow(row)
        root.create_download_progress(info=info)

    def paint(self, painter, option, index):
        if not self.parent().indexWidget(index):
            open_button = QPushButton(self.parent())
            open_button.setText("打开")
            open_button.clicked.connect(lambda: self.button_callback(index))

            reconnect_button = QPushButton(self.parent())
            reconnect_button.setText("重试")
            reconnect_button.clicked.connect(lambda: self.reconnect(index))
           
            open_button.index = [index.row(), index.column()]
            reconnect_button.index = [index.row(), index.column()]
            
            h_box_layout = QHBoxLayout()
            h_box_layout.addWidget(open_button)
            h_box_layout.addWidget(reconnect_button)
            
            h_box_layout.setContentsMargins(0, 0, 0, 0)
            h_box_layout.setAlignment(Qt.AlignCenter)
            widget = QWidget()
            widget.setLayout(h_box_layout)
            self.parent().setIndexWidget(
                index,
                widget
            )


class TableView(QTableView):
    def __init__(self, parent=None, *args, **kwargs):
        super(TableView, self).__init__(parent, *args, **kwargs)
        self.info = {}
        self.table_head = ['文件', '下载状态', '进度', '操作']
        #self.setAlternatingRowColors(True)
        self.verticalHeader().hide()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setItemDelegateForColumn(3, Operate_Button(self))
        self.setupUi()

    def setupUi(self):
        columns = len(self.table_head)
        self._model = QStandardItemModel(0, columns)
        self._model.setHorizontalHeaderLabels(self.table_head)
        self.setModel(self._model)
        #self.horizontalHeader().setStyleSheet("QHeaderView::section{background-color:rgba(0, 0, 0, 0);font:13pt '宋体';color: white;};")
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def translate_file_size(self, value):
        unit_box = iter(['B', 'K', 'M', 'G'])
        value_lenth = len(str(value))
        unit = next(unit_box)
        while value_lenth > 3:
            value = value / 1024
            value_lenth = len(str(int(value)))
            unit = next(unit_box)
        return (round(value, 2), unit)

    def set_row_item_object_name(self, row, color):
        self._model.item(row, 0).setForeground(color)
        self._model.item(row, 1).setForeground(color)
        self._model.item(row, 2).setForeground(color)

    def count_process(self, image_size, file, d_timer_id, file_name):
        row = self.info[d_timer_id]
        print(f"row = {row}")
        value = 0
        if os.path.exists(file):
            file_size = os.path.getsize(file)
            if image_size != -1:
                value = int((file_size/image_size)*100)
                value = f"{value}%"
            else:
                value, unit = self.translate_file_size(file_size)
                value = f"{value}{unit}"

            download_status = "下载中"
        else:
            download_status = "等待下载"
        self._model.setItem(row, 2, My_Item(value))
        self._model.setItem(row, 1, My_Item(download_status))
        
        # self._model.item(row, 1).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        # self._model.item(row, 2).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        
    def set_download_final_status(self, info):
        isSuccess = info['isSuccess']
        timer_box = info['timer_box']
        d_timer_id = info['download_timer_id']
        row = self.info[d_timer_id]
        timer_box[d_timer_id].stop()
        if not isSuccess:
            self._model.setItem(row, 1, My_Item("下载失败"))
            self.set_row_item_object_name(row, QBrush(QColor('red')))

        else:
            self._model.setItem(row, 1, My_Item("下载完成"))
            self._model.setItem(row, 2, My_Item("100%"))
            self.set_row_item_object_name(row, QBrush(QColor('lightgreen')))
            #self.set_row_item_font_color(row, 'lightgreen')
            #self._model.item(row, 2).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        
        #self._model.item(row, 1).setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        

    def set_item(self, image_size, file, timer_box, d_timer_id, file_name, main, dontDownload=False):
        if image_size is None:

            self.info[d_timer_id] = row = self.info.get(d_timer_id, self.model().rowCount())
            info = {
                    'file_name': file_name, 
                    'file': file, 
                    'd_timer_id': d_timer_id, 
                    'main': main,
                    'image_size': image_size,
                    'timer_box': timer_box,
                    'row': row,
                    }
            self._model.setItem(row, 0, My_Item(file_name, info=info))
            self._model.setItem(row, 1, My_Item('等待下载'))
            self._model.setItem(row, 2, My_Item('0%'))

        else:
            timer_box[d_timer_id] = QTimer()
            timer_box[d_timer_id].timeout.connect(
                lambda: self.count_process(image_size, file, d_timer_id, file_name))
            if not dontDownload:
                timer_box[d_timer_id].start(1000)
            else:
                info = {}
                info['isSuccess'] = True
                info['timer_box'] = timer_box
                info['download_timer_id'] = d_timer_id
                self.set_download_final_status(info)
        
 
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    qb = TableView()
    file_name = file = d_timer_id = main = ''
    for row in range(1, 6):
        for col in range(4):
            info = {'file_name': file_name, 'file': file, 'd_timer_id': d_timer_id, 'main': main}
            qb._model.setItem(row-1, col, My_Item(f"{row}, {col}", info=info))
            
    qb.show()
    sys.exit(app.exec_())
