#!/usr/bin/env python3


def single_instance(cls):
    def single(*args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance
    return single