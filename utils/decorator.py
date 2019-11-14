# -*- coding: utf-8 -*-

from __future__ import absolute_import
import functools
import os
import re
import json
import wrapt
import time
# from message_queue.tasks import new_template_task
# from types import GeneratorType
# from items.base_item import BaseItem
# from templates.template import Template


def retry(retry_count=0, logger=None):
    """
    重试次数的装饰器
    :param retry_count: 次数
    :param logger: logger
    :return: 装饰函数
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while count < retry_count:
                try:
                    res = func(*args, **kwargs)
                    return res
                except Exception as e:
                    count += 1
        return wrapper
    return decorator


def callback(callback=None):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            resp = wrapped(*args, **kwargs)
            if callback:
                callback(resp)
        except Exception as e:
            raise e
    return wrapper


def check_path(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            if os.path.exists(path):
                func(path)
            else:
                raise FileExistsError("Not find file.")
        return wrapper
    return decorator


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton


def item_format(file):
    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        try:
            with open(file, mode='r', encoding='utf-8') as f:
                d = []
                for line in f.readlines():
                    k, v = line.split('=')
                    d.append({k, v.replace('\n', '')})
                wrapped(d)
        except Exception as e:
            raise e

    return wrapper


# def put_request(*args, **kwargs):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*kargs, **kkwargs):
#             kargs = args
#             kkwargs = kwargs
#             try:
#                 return func(*kargs, **kkwargs)
#             except Exception as e:
#                 logger.error(e)
#         return wrapper
#     return decorator


# def put_task(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             result = func(*args, **kwargs)
#             if isinstance(result, Template):
#                 new_template_task(result)
#             elif isinstance(result, list) or isinstance(result, GeneratorType):
#                 for res in result:
#                     new_template_task(res)
#         except Exception as e:
#             logger.error(e)
#     return wrapper


# def put_data(pipeline=None, *arguments, **parameters):
#     def decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 result = func(*args, **kwargs)
#                 if isinstance(result, BaseItem):
#                     pp = pipeline(*arguments, **parameters)
#                     pp.before_process()
#                     pp.process(item=result)
#                     pp.after_process()
#                 elif isinstance(result, list) or isinstance(result, GeneratorType):
#                     pp = pipeline(*arguments, **parameters)
#                     pp.before_process()
#                     for item in result:
#                         pp.process(item=item)
#                     pp.after_process()
#                 else:
#                     logger.info('func>>>%s ' % str(func))
#             except Exception as e:
#                 logger.error(e)
#         return wrapper
#     return decorator


def _get_last_backslash(strings, regex=re.compile(r"\\*$")):
    mth = regex.search(strings)
    if mth:
        return mth.group()
    return ""


def replace_quote(json_str):
    """
    将要被json.loads的字符串的单引号转换成双引号，
    如果该单引号是元素主体，而不是用来修饰字符串的。则不对其进行操作。
    :param json_str:
    :return:
    """
    if not isinstance(json_str, str):
        return json_str

    double_quote = []
    new_lst = []
    for index, val in enumerate(json_str):
        if val == '"' and not len(_get_last_backslash(json_str[:index])) % 2:
            if double_quote:
                double_quote.pop(0)
            else:
                double_quote.append(val)
        if val == "'" and not len(_get_last_backslash(json_str[:index])) % 2:
            if not double_quote:
                val = '"'
        new_lst.append(val)
    return "".join(new_lst)


def safely_json_loads(json_str, defaulttype=dict, escape=True):
    """
    返回安全的json类型
    :param json_str: 要被loads的字符串
    :param defaulttype: 若load失败希望得到的对象类型
    :param escape: 是否将单引号变成双引号
    :return:
    """
    if not json_str:
        return defaulttype()
    elif escape:
        data = replace_quote(json_str)
        return json.loads(data)
    else:
        return json.loads(json_str)


def retry_wrapper(
        retry_times, exception=Exception, error_handler=None, interval=0.1):
    """
    函数重试装饰器
    :param retry_times: 重试次数
    :param exception: 需要重试的异常
    :param error_handler: 出错时的回调函数
    :param interval: 重试间隔时间
    :return:
    """
    def out_wrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    count += 1
                    if error_handler:
                        result = error_handler(
                            func.__name__, count, e, *args, **kwargs)
                        if result:
                            count -= 1
                    if count >= retry_times:
                        raise
                    time.sleep(interval)
        return wrapper
    return out_wrapper