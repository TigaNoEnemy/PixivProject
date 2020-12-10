#!/usr/bin/env python3
# 负责获取token、token加密、token解密、
# token覆写、记录下次是否自动登录

import hashlib
import sqlite3
from pyDes import des, CBC, PAD_PKCS5
from binascii import b2a_hex, a2b_hex
import uuid
from datetime import datetime
import os
import sys

from utils.Single_Instance import single_instance

import cgitb
cgitb.enable(format='text', logdir='log_file')

@single_instance
class login_info_parser:
    _instance = None
    def __init__(self):
        dir_md5 = hashlib.md5('Pixiv'.encode())
        dir_hex = dir_md5.hexdigest()
        if sys.platform == 'linux':
            home = os.path.expandvars("$HOME")
            loging_token_dir = f"{home}/{dir_hex}"
        else:
            home = os.path.expandvars("$APPDATA")
            loging_token_dir = f"{home}/{dir_hex}"

        self.loging_token_dir = loging_token_dir
        self.login_token_file = f"{loging_token_dir}/{dir_hex}"
        self.check_file()
        self.key = uuid.UUID(int=uuid.getnode()).hex[-8:]

    def update_token(self, pixiv_id, user, login_account, access_token, next_time_auto_login):
        des_obj = des(self.key, CBC, self.key, pad=None, padmode=PAD_PKCS5)
        access_token = des_obj.encrypt(access_token, padmode=PAD_PKCS5)
        access_token = b2a_hex(access_token).decode('utf-8')
        _datetime = datetime.now()
        conn = sqlite3.connect(self.login_token_file)
        cur = conn.cursor()
        try:
            cur.execute('''create table USER(
                id int primary key, 
                pixiv_id int unique,
                login_account varchar(255),
                user varchar(255) unique, 
                access_token varchar(255), 
                next_time_auto_login boolean, 
                login_time datetime
                )''')
            
        except Exception as e:
            print(f"creat error <{e}>")
        try:
            cur.execute(f'insert into USER(id, pixiv_id, login_account, user, access_token, next_time_auto_login, login_time) values(1, 0, "0", "0", "0", 0, "{_datetime}")')
        except Exception as e:
            print(f"insert error <{e}>")

        if login_account:
            query = f'update USER set access_token="{access_token}", next_time_auto_login={next_time_auto_login}, login_time="{_datetime}", user="{user}", pixiv_id={pixiv_id}, login_account="{login_account}" where id=1'
        else:
            query = f'update USER set access_token="{access_token}", next_time_auto_login={next_time_auto_login}, login_time="{_datetime}", user="{user}", pixiv_id={pixiv_id} where id=1'
        print(query)
        cur.execute(query)
        cur.close()
        conn.commit()
        conn.close()

    def get_token(self):
        des_obj = des(self.key, CBC, self.key, pad=None, padmode=PAD_PKCS5)
        conn = sqlite3.connect(self.login_token_file)
        cur = conn.cursor()

        try:
            user_box = cur.execute(f"select * from USER where id=1;")
        except:
            token = None
            auto = False
            login_account = ""
        else:
            try:
                token = user_box.__next__()
            except StopIteration:
                login_account = ""
                token = None
                auto = False
            else:
                auto = token[5]
                login_account = token[2]
                token = token[4].encode('utf-8')     

        cur.close()
        conn.commit()
        conn.close()
        if token:
            try:
                token = des_obj.decrypt(a2b_hex(token), padmode=PAD_PKCS5).decode('utf-8')
            except UnicodeDecodeError:
                if os.path.exists(self.login_token_file):
                    os.remove(self.login_token_file)
                token = None
        print('Complete: get_token')
        return {'token': token, 'auto': auto, 'login_account': login_account}

    def check_file(self):
        if not os.path.exists(self.loging_token_dir):
            os.mkdir(self.loging_token_dir)

if __name__ == '__main__':
    login = login_info_parser()
    login.update_token(123, 'test', 'test', 1)
    print(login.get_token())
