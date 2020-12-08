#!/usr/bin/env python3


class My_Meta_Class(type):
    """使用元类实现单例模式，较有保障"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = None

    def __call__(self, *arg, **kwargs):
        if not self._instance:
            self._instance = super().__call__()

        return self._instance
