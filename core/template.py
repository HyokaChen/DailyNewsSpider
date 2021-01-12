#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : template.py
 @Time       : 2019-04-16 21:29
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import os
import codecs
import json
from datetime import datetime
from config.constant import DAILY_FORMAT


class HyokaTemplate(object):
    """
    模板实体类
    """

    def __init__(self, data_dict):
        assert data_dict.get("START_URL", None), "起始链接为空！"
        assert data_dict.get("START_URL", ""), "起始链接为空！"
        self.START_URL = data_dict.get("START_URL")
        self.METHOD = data_dict.get("METHOD", "GET")
        self.REFERER = data_dict.get("REFERER", None)
        assert data_dict.get("SPIDER_NAME", None), "爬虫名称需要指定！"
        assert data_dict.get("SPIDER_NAME", ""), "爬虫名称需要指定！"
        self.SPIDER_NAME = data_dict.get("SPIDER_NAME")
        assert data_dict.get("SITE_NAME", None), "网站名称需要指定！"
        assert data_dict.get("SITE_NAME", ""), "网站名称需要指定！"
        self.SITE_NAME = data_dict.get("SITE_NAME")
        self.CATEGORY = data_dict.get("CATEGORY", None)
        self.RENDER = data_dict.get("RENDER", False)
        self.TIMEOUT = data_dict.get("TIMEOUT", 0)
        self.SLEEP_TIME = data_dict.get("SLEEP_TIME", 0)
        self.SESSION = data_dict.get("SESSION", False)
        self.MAX_SESSION_TIMES = data_dict.get("MAX_SESSION_TIMES", 10)
        self.RANGE_TIME = (
            data_dict.get("RANGE_TIME")
            if data_dict.get("RANGE_TIME") != ""
            else datetime.now().strftime(DAILY_FORMAT) + "#"
        )
        self.RETURN_TYPE = data_dict.get("RETURN_TYPE", "text")
        self.DATA_TABLE = data_dict.get("DATA_TABLE", None)
        self.PRIORITY = data_dict.get("PRIORITY", 0)
        self.IS_DUPLICATE = data_dict.get("IS_DUPLICATE", False)
        # 请求模板集合
        assert data_dict.get("REQUESTS", None), "请求模板不能为空！"
        assert data_dict.get("REQUESTS", []), "请求模板不能为空！"
        self.TEMPLATES = data_dict.get('REQUESTS', None)
        # 处理函数集合
        assert data_dict.get("PROCESSES", None), "处理模板不能为空！"
        assert data_dict.get("PROCESSES", []), "处理模板不能为空！"
        self.PROCESSES = data_dict.get('PROCESSES', None)
        # 结果模板集合
        assert data_dict.get("RESULTS", None), "结果模板不能为空"
        assert data_dict.get("RESULTS", []), "结果模板不能为空"
        self.RESULTS = data_dict.get('RESULTS', None)


class ReadTemplateJson(object):
    """
    读取模板实体
    """

    @staticmethod
    def read_all_template(dir_path) -> list:
        """
        读取templates路径下的所有json模板文件
        :return: 模板实体对象集合
        """
        if 'Template' in str(dir_path) and ".json" in str(dir_path):
            with codecs.open(dir_path, encoding="utf-8") as f:
                _temp_dict = json.load(f)
            yield _temp_dict  # HyokaTemplate(_temp_dict)
        else:
            # yaml.safe_load('xx.yaml')
            all_files = os.listdir(dir_path)
            for file in all_files:
                if 'Template' in str(file) and ".json" in str(file):
                    file_path = "{path}{template_name}".format(path=dir_path, template_name=file)
                    print('===>' + file_path)
                    if not os.path.exists(file_path):
                        raise FileExistsError("Path is error!")
                    with codecs.open(file_path, encoding="utf-8") as f:
                        _temp_dict = json.load(f)
                    yield _temp_dict  # HyokaTemplate(_temp_dict)

    @staticmethod
    def load_template_by_name(dir_path: str, name: str):
        """
        加载模板实体
        :param dir_path: 路径
        :param name: 名称
        :return: 模板实体对象
        """
        path = "{0}" + os.sep + "{name}.json".format(dir_path, name=name)
        if not os.path.exists(path):
            assert None, "{name}.json is not in templates folder".format(name=name)
        if not os.path.exists(path):
            raise FileExistsError("Path is error!")
        with codecs.open(path, encoding="utf-8") as f:
            _temp_dict = json.load(f)
        return _temp_dict  # HyokaTemplate(_temp_dict)