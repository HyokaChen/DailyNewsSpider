#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : pipeline.py
 @Time       : 2019-04-16 21:29
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from utils.color import Colored
import json
from config.constant import STORE_TOPIC
from utils.db_util import rdb


class ProcessContent(object):
    def content_process(self, content):
        raise NotImplementedError


class MysqlProcessContent(ProcessContent):
    def content_process(self, content):
        pass


class RedisProcessContent(ProcessContent):
    def content_process(self, content):
        item = json.dumps(content, ensure_ascii=False)
        rdb.sadd(STORE_TOPIC, item)
