#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : http_result.py
 @Time       : 2018/12/15 0015 17:04
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from utils.color import Colored


class HTTPResultTemplate(object):
    __slots__ = [
        'result_id',
        'field_dict',
        'global_parameter'
    ]

    def __init__(self, result_id, field_dict=None, global_parameter=None):
        self.result_id = result_id
        self.field_dict = field_dict
        self.global_parameter = global_parameter

    def __str__(self):
        return Colored.yellow("[%s] <Result>" % self.result_id)

    def __contains__(self, item):
        return True if item.result_id == self.result_id else False

    def obj2dict(self):
        return {
            'result_id': self.result_id,
            'field_dict': self.field_dict,
            'global_parameter': self.global_parameter
        }

    @staticmethod
    def dict2obj(dict_content):
        return HTTPResultTemplate(**dict_content)
    __repr__ = __str__

