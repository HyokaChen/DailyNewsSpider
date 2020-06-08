# -*- coding: utf-8 -*-
from __future__ import absolute_import
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from hashlib import md5
import os
import json
import pickle
import sys
from datetime import datetime
from utils.user_agents import UserAgent
from config.constant import DAILY_FORMAT
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def generate_token(*contents):
    """
    生成以md5加密的hash值
    :param contents: 需要加密的内容
    :return: md5加密的hash值
    """
    m = md5()
    for content in contents:
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        m.update(content.encode('utf-8'))
    return m.hexdigest()


def create_folder(path):
    """
    创建文件夹
    :param path: 路径
    :return: None
    """
    if not os.path.exists(path):
        os.mkdir(path)


def is_file_exists(path):
    """
    判断文件或者文件夹是否存在
    :param path: 路径
    :return: True or False
    """
    return os.path.exists(path)


def decode_content(content, encoding=None):
    """
    解码内容为文本
    :param content: 二进制内容
    :param encoding: 编码
    :return: 文本
    """
    try:
        if encoding is not None:
            return content.decode(encoding)
        return content.decode('utf-8')
    except Exception:
        try:
            return content.decode('gbk')
        except Exception as e:
            raise e


def dumps_content(content):
    """
    pickle 序列化响应对象
    :param content: 响应对象
    :return: 序列化内容
    """
    return pickle.dumps(content)


def loads_content(content):
    """
    pickle 反序列化响应对象
    :param content: 序列化内容
    :return: 响应对象
    """
    return pickle.loads(content)


def get_start_end_date(date_str):
    """
    提取模板中的起止时间
    :param date_str: 时间 str
    :return: 起始时间，结束时间
    """
    date_list = date_str.split("#")
    if len(date_list) == 1:
        raise Exception("range time must append #")
    start_date = date_list[0]
    if date_list[1] != "":
        end_date = date_list[1]
    else:
        end_date = datetime.now().strftime(DAILY_FORMAT)

    return start_date, end_date