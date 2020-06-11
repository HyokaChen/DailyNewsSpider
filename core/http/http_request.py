#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : http_request.py
 @Time       : 2018/12/14 0014 22:18
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from utils.color import Colored
from config.constant import HTML, GET


class HTTPRequestTemplate(object):
    __slots__ = ['request_id',
                 'start_url',
                 'method',
                 'post_data',
                 'referer',
                 'process',
                 'parameters',
                 'category',
                 'timeout',
                 'sleep_time',
                 'render',
                 'use_proxy',
                 'cookies',
                 'return_type',
                 'return_item',
                 'is_duplicate',
                 'is_multiple',
                 'result',
                 'next_request',
                 'parallel_request',
                 'stopped',
                 'extra_headers',
                 ]

    def __init__(self, request_id, start_url=None, method=GET, post_data=None,
                 referer=None, process=None, parameters=None,
                 category="", timeout=None, sleep_time=0.5, render=False,
                 use_proxy=None, cookies=None, return_type=HTML,
                 return_item=None, is_duplicate=False, is_multiple=False,
                 result=None, next_request=None, parallel_request=None, stopped=None, extra_headers=None):
        self.request_id = request_id
        self.start_url = start_url
        self.method = method
        self.post_data = post_data
        self.referer = referer
        self.process = process
        self.parameters = parameters
        self.category = category
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.render = render
        self.use_proxy = use_proxy
        self.cookies = cookies
        self.return_type = return_type
        self.return_item = return_item
        self.is_duplicate = is_duplicate
        self.is_multiple = is_multiple
        self.result = result
        self.next_request = next_request
        self.parallel_request = parallel_request
        self.stopped = stopped
        self.extra_headers = extra_headers

    def __str__(self):
        return Colored.yellow("[%s] <Request [%s] [%s]>" % (self.request_id,
                                                            self.method, self.start_url))

    def __contains__(self, item):
        return True if item.request_id == self.request_id else False

    def obj2dict(self):
        return {
            'request_id': self.request_id,
            'start_url': self.start_url,
            'method': self.method,
            'post_data': self.post_data,
            'referer': self.referer,
            'process': self.process,
            'parameters': self.parameters,
            'category': self.category,
            'timeout': self.timeout,
            'sleep_time': self.sleep_time,
            'render': self.render,
            'use_proxy': self.use_proxy,
            'cookies': self.cookies,
            'return_type': self.return_type,
            'return_item': self.return_item,
            'is_duplicate': self.is_duplicate,
            'is_multiple': self.is_multiple,
            'result': self.result,
            'next_request': self.next_request,
            'parallel_request': self.parallel_request,
            'stopped': self.stopped,
            'extra_headers': self.extra_headers
        }

    @staticmethod
    def dict2obj(dict_content):
        return HTTPRequestTemplate(**dict_content)

    __repr__ = __str__
