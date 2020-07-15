#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil

def move_file():
    keyword = "Created by: PyQt5 UI code generator 5.14.2"
    path = '.'

    a = os.listdir('.')
    for i in a:
        if i.endswith('.py'):
            f = open(f'{path}/{i}', encoding='utf-8')
            b = f.read()
            if keyword in b:
                try:
                    shutil.move(f'{path}/{i}', f"{path}/qtcreatorFile/{i}")
                except:
                    pass
            f.close()
        if i.endswith('ui'):
            try:
                shutil.move(f'{path}/{i}', f"{path}/qtcreatorFile/{i}")
                print(i)
            except:
                pass

def remove_file():
    path = '.'

    a = os.listdir('.')
    b = os.listdir(f"{path}/qtcreatorFile")
    for i in a:
        if i in b:
            try:
                print(i)
                os.remove(f"{path}/{i}")
            except:
                pass

if __name__ == '__main__':
    move_file()