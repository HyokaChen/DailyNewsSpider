#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : new_sina_spider.py
 @Time       : 2019-05-08 07:54
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""


def first_process(response):
    return response


def second_process(response, parameters):
    print(parameters.get('page'))
    return response