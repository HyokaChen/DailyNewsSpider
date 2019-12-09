#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : __init__.py.py
 @Time       : 2019-04-16 21:18
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import os
import sys
import re
import logme
from types import GeneratorType
from lxml.etree import _Element
import time
from hashlib import md5
from datetime import datetime
from dateutil.parser import parse
from config.constant import (TYPE_FUNC_MAP, SITE_MAP, SiteType, DATE_FMT, ES_DATE_FMT, NATIONALITY, ASTROLOGY,
                             LEFT_BRACKET, RIGHT_BRACKET, COLON, DIAGONAL, GREATER_THAN, TEXT, HASH, LIST,
                             ONE)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def is_in_range_time(c_date, s_date, e_date):
    if isinstance(c_date, str):
        try:
            timestamp = float(c_date)
            c_date = datetime.fromtimestamp(timestamp)
        except:
            c_date = parse(c_date.strip())
    if isinstance(s_date, str):
        s_date = parse(s_date.strip())
    if isinstance(e_date, str):
        e_date = parse(e_date) if e_date.strip() != '' else datetime.now()
    return True if s_date <= c_date <= e_date else False


def sort_time(time_list):
    wait_sort_dict = dict()
    for index, c_date in enumerate(time_list):
        if isinstance(c_date, str):
            try:
                timestamp = float(c_date)
                c_date = datetime.fromtimestamp(timestamp)
            except:
                c_date = parse(c_date.strip())
            wait_sort_dict.setdefault(index, c_date)
    sort_dict = sorted(wait_sort_dict.items(), key=lambda item: item[1], reverse=True)
    return [arg for arg, val in sort_dict]


def process_raw_value(raw_value, type_value):
    """
    处理item的定义配置
    :param raw_value: 原始字段数据
    :param type_value: item定义的类型
    :return: 转换成item需要的数据类型，并返回
    """
    value = None
    try:
        if isinstance(raw_value, GeneratorType):
            if type_value == 'list':
                value = TYPE_FUNC_MAP[type_value](raw_value)
            else:
                value = TYPE_FUNC_MAP[type_value](next(raw_value))
        else:
            value = TYPE_FUNC_MAP[type_value](raw_value)
    except StopIteration:
        pass
    except Exception as e:
        raise e
    finally:
        return value


def format_data(data, node_path, reg_idx=ONE):
    """
    按照数据处理路径（xpath或者json）处理数据
    :param data: 原始数据
    :param node_path: 处理路径，可以是xpath，或者json
    :param reg_idx: 正则提取的要求
    :return: 处理路径指定需要的数据
    """
    result = None
    print('**********{0}'.format(node_path))
    if isinstance(node_path, str) and node_path != "":
        if COLON in node_path:
            node, attr = node_path.split(COLON)
            results = data.select(node)
            if len(results) > 0:
                result = results[0]
                if attr == TEXT:
                    result = result.get_text('\n\n', strip=True).strip()
                else:
                    result = result.attrs[attr].strip()
            else:
                result = ""
        elif GREATER_THAN in node_path and isinstance(data, dict):
            node, *list_or_one_list = node_path.split(HASH)
            json_nodes = [n for n in node.split(">") if n != '']
            result = _transform_json_content(data, json_nodes)
            if len(list_or_one_list) > 0:
                list_or_one = list_or_one_list[0]
                if ONE == list_or_one:
                    result = result[0]
        elif DIAGONAL in node_path and isinstance(data, _Element):
            node, *list_or_one_or_text_list = node_path.split(HASH)
            result = data.xpath(node)
            if len(result) == 0:
                result = None
            elif len(list_or_one_or_text_list) > 0:
                list_or_one_or_text = list_or_one_or_text_list[0]
                if TEXT == list_or_one_or_text:
                    result = '\n'.join(result).strip()
                elif LIST == list_or_one_or_text:
                    result = result
                elif ONE == list_or_one_or_text:
                    result = result[0].strip()
            else:
                result = result[0].strip()
        elif isinstance(data, str):
            results = re.findall(node_path, data)
            if LIST == reg_idx:
                result = results
            elif ONE == reg_idx:
                result = results[0]
        else:
            raise Exception("format type is not right or data is not <_Element> or type <dict>!!!")
    return result


def _transform_json_content(data, nodes: list):
    """
    处理a>b>c的json指示符
    :param data: 字典数据
    :param nodes: 指示符
    :return: a>b>c返回的指示数据
    """
    results = []

    def _get_data(inner_data, inner_nodes):
        # 如果路径没了，返回本身合并成的list
        try:
            if len(inner_nodes) == 1:
                results.append(inner_data.get(inner_nodes[0]))
            else:
                node = inner_nodes[0]
                del inner_nodes[0]
                inner_nodes = inner_nodes
                temp_data = inner_data.get(node)
                if isinstance(temp_data, list):
                    # 如果数据是list的形式，则单个继续递归
                    for da in temp_data:
                        _get_data(da, inner_nodes)
                else:
                    # 如果nodes还有个数，对于单个来说继续递归
                    _get_data(temp_data, inner_nodes)
        except Exception as e:
            raise e
    _get_data(data, nodes)
    return results


def transform_datetime(date_str, site):
    """
    根据site转换原始的date为正规的date类型存放
    :param date_str: 原始的date
    :param site: 网站标识
    :return: 转换后的date
    """
    result = None
    if site in SITE_MAP:
        if SITE_MAP[site] == SiteType.SINA:
            try:
                time_int = int(date_str)
                result = datetime.fromtimestamp(time_int).strftime(DATE_FMT)
            except Exception as e:
                result = parse(date_str).strftime(DATE_FMT)
        elif SITE_MAP[site] == SiteType.TENCENT:
            result = date_str
        elif SITE_MAP[site] == SiteType.TUICOOL:
            result = date_str
        elif SITE_MAP[site] == SiteType.HACKER:
            result = date_str
        elif SITE_MAP[site] == SiteType.DMZJ:
            result = parse(date_str).strftime(DATE_FMT)
        elif SITE_MAP[site] == SiteType.ACGMH:
            result = parse(date_str).strftime(DATE_FMT)
        elif SITE_MAP[site] == SiteType.CTOLIB:
            result = parse(date_str).strftime(DATE_FMT)
        elif date_str.strip() == '':
            result = datetime.now().strftime(DATE_FMT)
    else:
        result = parse(date_str).strftime(DATE_FMT)
    return result


@logme.log(name="[to_dict_2]")
def to_dict_2(result, logger=None):
    """
    item进行进一步的更新，添加一些记录字段
    :param result: 原始的item数据
    :param logger: 日志记录
    :return: 返回最终的item
    """
    try:
        m = md5()
        d = dict()
        for k1, k2 in result.items():
            # 以url的md5作为唯一性标识
            if k1 == 'url':
                m.update(k2.strip().encode('utf-8'))
                d.setdefault('_id', m.hexdigest())
                d.setdefault('url', k2.strip())
            elif k1 == 'nationality':  # 国籍地区
                if isinstance(k2, list):
                    nationality = ';'.join([NATIONALITY[str(num).strip()] for num in k2])
                else:
                    nationality = NATIONALITY[str(k2).strip()]
                d.setdefault(k1, nationality)
            elif k1 == 'astrology':  # 星座
                d.setdefault(k1, ASTROLOGY[str(k2).strip()])
            elif LEFT_BRACKET in k2 and RIGHT_BRACKET in k2:
                # 类似于["制作人", "编剧"]
                temp_k2 = k2.strip().replace('"', '').replace("'", '')\
                    .replace(LEFT_BRACKET, '')\
                    .replace(RIGHT_BRACKET, '')
                temp_values = ';'.join([temp.strip() for temp in temp_k2.split(',')])
                d.setdefault(k1, temp_values)
            elif isinstance(k2, list):
                temp_values = ';'.join([str(k).strip() for k in k2])
                d.setdefault(k1, temp_values)
            else:
                d.setdefault(k1, str(k2).strip())

        # 添加新闻日期转换
        if 'news_time' in d:
            # 新闻日期添加，不是int类型
            news_time = transform_datetime(d['news_time'], d['site'])
            d.update({'news_time': news_time})
        # 添加爬取的时间戳
        d.setdefault("timestamp", int(time.time() * 1000))

        # 添加最近更新的时间，后续item的更改需要同时更新这个字段
        d.setdefault(
            "last_modified", datetime.utcnow().strftime(ES_DATE_FMT)
        )
        return d
    except Exception as e:
        logger.error("[to_dict_2]发生错误，链接为：{0}".format(result['url']), exc_info=True)
    return None


__all__ = [
    'format_data',
    'is_in_range_time',
    'to_dict_2',
    'process_raw_value',
    'sort_time',
]