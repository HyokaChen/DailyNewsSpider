#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : constant.py
 @Time       : 2019-04-16 21:25
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import os
import sys
from enum import Enum, unique
from envparse import env


@unique
class EnvironmentType(Enum):
    DEV = 0
    PROD = 1


@unique
class SiteType(Enum):
    SINA = 0
    TENCENT = 1
    TUICOOL = 2
    HACKER = 3
    DMZJ = 4
    ACGMH = 5
    CTOLIB = 6
    PAPERSWITHCODE = 7
    HACKERNEWS = 8


@unique
class SpiderStatus(Enum):
    Null = 0
    Start = 1
    Stopping = 2
    Stopped = 3


@unique
class WayType(Enum):
    LPUSH = 0
    RPOP = 1
    HSET = 2
    HGET = 3
    SET = 4
    GET = 5
    SADD = 6
    SPOP = 7
    LLEN = 8
    SCARD = 9
    SRANDMEMBER = 10
    HKEYS = 11
    HDEL = 12


@unique
class StatusType(Enum):
    NONE = 0
    SUCCESS = 1
    FAIL = 2


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
ENVIRONMENT = EnvironmentType.DEV
if ENVIRONMENT == EnvironmentType.DEV:
    env.read_envfile('{0}/.env.dev'.format(CURRENT_DIR))
elif ENVIRONMENT == EnvironmentType.PROD:
    env.read_envfile('~/.env.prod')
# 配置文件
MONGODB_HOST = env('MONGODB_HOST')
MONGODB_PORT = env.int('MONGODB_PORT')
MONGODB_USER = env('MONGODB_USER')
MONGODB_PWD = env('MONGODB_PWD')
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env.int('REDIS_PORT')
REDIS_PWD = env('REDIS_PWD')

# 模板解析字段
REQUESTS_DOT = 'REQUESTS.'
PROCESSES_DOT = 'PROCESSES.'
RESULTS_DOT = 'RESULTS.'
DOT = '.'
DOLLAR = '$'
AND = '&'
AT = '@'
HASH = '#'
DIAGONAL = '//'
GREATER_THAN = '>'
LESS_THAN = '<'
UNDER_LINE = '_'
LEFT_BRACE = '{'
RIGHT_BRACE = '}'
LEFT_BRACKET = '['
RIGHT_BRACKET = ']'
PERCENT = '%'
COLON = '::'
HALF_COLON = ':'

# 解析内容类型
TEXT = "text"
CSS = 'css'
JSON = "json"
HTML = "html"
LIST = 'list'
ONE = 'one'
GET = 'GET'
POST = 'POST'

# 排除字段
EXCLUDE_FIELD = {"id", "insert_time", "timestamp",
                 "global_parameter",
                 "result_id", "process_id",
                 "template_id"}

# 类型转换
TYPE_FUNC_MAP = {
    'int': int,
    'list': list,
    'str': str,
    'default': str
}

# 时间格式
DAILY_FORMAT = "%Y-%m-%d"
DATE_FMT = '%Y-%m-%d %H:%M:%S'
ES_DATE_FMT = '%Y-%m-%dT%H:%M:%S.000Z'

# 网站
SITE_MAP = {
    'sina': SiteType.SINA,
    'tencent': SiteType.TENCENT,
    'tuicool': SiteType.TUICOOL,
    'hacker': SiteType.HACKER,
    'dmzj': SiteType.DMZJ,
    'acgmh': SiteType.ACGMH,
    'ctolib': SiteType.CTOLIB,
    'paperswithcode': SiteType.PAPERSWITHCODE,
    "hackernews": SiteType.HACKERNEWS
}

# 消息队列
TEMPLATES_TOPIC = "templates"
REQUESTS_TOPIC = "requests_{0}"
PROCESSES_TOPIC = "processes_{0}"
RESULTS_TOPIC = "results_{0}"
TASK_TOPIC = 'task_{0}'
STORE_TOPIC = 'store'
REQUESTS = 'REQUESTS'
PROCESSES = 'PROCESSES'
RESULTS = 'RESULTS'
HASH_MAP = 'hash_map_{0}'
DOWNLOAD_STREAM = 'download_stream'
PROCESS_STREAM = 'process_stream'
RESULT_STREAM = 'result_stream'
MAX_LEN = 2000

# 类别
NEWS = 'news'
MUSIC = 'music'
VIDEO = 'video'
IMAGE = 'image'
WEIBO = 'weibo'
QZONE = 'qzone'

# 推送
PUBLISHED = "article-{0}-node"

NATIONALITY = {
    '': '未知',
    '1': '中国',
    '2': '中国台湾',
    '3': '中国香港',
    '4': '日本',
    '5': '韩国',
    '6': '美国',
    '7': '英国',
    '8': '德国',
    '9': '法国',
    '10': '印度',
    '11': '瑞典',
    '12': '挪威',
    '13': '朝鲜',
    '14': '越南',
    '15': '伊朗',
    '16': '古巴',
    '17': '希腊',
    '18': '巴西',
    '19': '捷克',
    '20': '泰国',
    '21': '波兰',
    '22': '荷兰',
    '23': '南非',
    '24': '意大利',
    '25': '奥地利',
    '26': '新西兰',
    '27': '墨西哥',
    '28': '俄罗斯',
    '29': '西班牙',
    '30': '新加坡',
    '31': '牙买加',
    '32': '马来西亚',
    '33': '澳大利亚',
    '34': '哥伦比亚',
    '35': '罗马尼亚',
    '40': '加拿大',
    '41': '塞尔维亚',
    '42': '格鲁吉亚',
    '43': '老挝',
    '44': '不丹',
    '45': '孟加拉',
    '46': '乌克兰',
    '47': '丹麦',
    '48': '缅甸',
    '49': '土耳其',
    '50': '比利时',
    '51': '瑞士',
    '52': '阿根廷',
    '53': '斯里兰卡',
    '54': '阿拉伯',
    '55': '匈牙利',
    '56': '智利',
    '57': '印度尼西亚',
    '58': '爱尔兰',
    '59': '菲律宾',
    '60': '尼日利亚',
    '61': '波多黎各',
    '62': '多米尼加共和国',
    '63': '尼泊尔',
    '64': '叙利亚',
    '65': '埃塞俄比亚',
    '66': '巴基斯坦',
    '68': '委内瑞拉',
    '69': '保加利亚',
    '70': '阿塞拜疆',
    '71': '以色列',
    '72': '贝宁',
    '73': '巴巴多斯',
    '74': '阿尔及利亚',
    '75': '芬兰',
    '76': '秘鲁',
    '77': '葡萄牙',
    '78': '立陶宛',
    '79': '埃及',
    '80': '蒙古',
    '81': '爱沙尼亚',
    '82': '波黑',
    '83': '斯洛伐克'
}

ASTROLOGY = {
    '': '未知',
    '1': '白羊座',
    '2': '金牛座',
    '3': '双子座',
    '4': '巨蟹座',
    '5': '狮子座',
    '6': '处女座',
    '7': '天秤座',
    '8': '天蝎座',
    '9': '射手座',
    '10': '摩羯座',
    '11': '水瓶座',
    '12': '双鱼座'
}
