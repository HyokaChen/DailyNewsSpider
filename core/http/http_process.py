#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : http_process.py
 @Time       : 2018/12/15 0015 16:50
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from utils.color import Colored


class HTTPProcessTemplate(object):
    __slots__ = ['process_id',
                 'process_method',
                 'parameters',
                 ]

    def __init__(self, process_id, process_method=None, parameters=None):
        self.process_id = process_id
        self.process_method = process_method
        self.parameters = parameters

    def __str__(self):
        return Colored.blue('<Process [{0}]:[{1}]>'.
                            format(self.process_id,
                                   self.process_method))

    def __contains__(self, item):
        return True if item.process_id == self.process_id else False

    def obj2dict(self):
        return {
            'process_id': self.process_id,
            'process_method': self.process_method,
            'parameters': self.parameters
        }

    @staticmethod
    def dict2obj(dict_content):
        return HTTPProcessTemplate(**dict_content)

    __repr__ = __str__
