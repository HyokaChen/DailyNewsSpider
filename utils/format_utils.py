#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : format_utils.py
 @Time       : 2017/10/15 0015 14:13
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import os
import importlib
from utils.db_util import find_data
from config.constant import CURRENT_DIR

DATE_FORMAT = {"short-term": "%Y-%M-%d", "slash": "%Y/%M/%d"}


def load_class(klass, path=None):
    if not path:
        path = "{0}/spiders".format(CURRENT_DIR)
    os.chdir(path)
    files = os.listdir(path)
    for file in files:
        name, *_ = file.partition("_")
        package = file.replace(".py", "")
        if name.capitalize() in klass:
            mod = importlib.import_module("spiders.{0}".format(package))
            return getattr(mod, klass)


def load_method(path):
    if path is None:
        return None
    package, method = path.rsplit('.', 1)
    module = importlib.import_module('{package}'.format(package=package))
    return getattr(module, method)


def load_item(path):
    collection, item_name = path.rsplit('.', 1)
    item_definition = find_data(collection, item_name)
    return item_definition


if __name__ == "__main__":
    load_class("TencentNewsIndexSpider")
