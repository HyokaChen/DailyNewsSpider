#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : download.py
 @Time       : 2019-04-16 21:30
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import logme
import random
import asyncio
import json
import cchardet as chardet
from utils.color import Colored
import httpx
from httpx import Response
from typing import Dict, List, Set, Coroutine, Any, Union
import time
from core.queue import Task
from utils import generate_token, create_folder, dumps_content, loads_content, is_file_exists
from utils import decode_content
from utils.proxy_utls import get_random_proxy
from lxml import etree
from bs4 import BeautifulSoup as bs
from config.constant import ENVIRONMENT, EnvironmentType, GET, POST, TEXT, JSON, CSS
from utils import UserAgent

ua = UserAgent()


@logme.log(name="Downloader")
# TODO: to use https://www.python-httpx.org/ to download web page
class Downloader(object):
    __slots__ = [
        'sleep_factor',
        'session_container'
    ]

    def __init__(self):
        super().__init__()
        self.sleep_factor = 2
        self.session_container = dict()

    def close(self):
        self.session_container.clear()

    __del__ = close

    async def single_download(self, task: Task):
        headers = {
            'User-Agent': ua.random
        }
        http_request = task.request
        if http_request['referer']:
            headers.setdefault('Referer', http_request['referer'])
        elif 'referer' in task.parameters:
            headers.setdefault('Referer', task.parameters["referer"])
        if http_request['extra_headers']:
            headers.update(http_request['extra_headers'])
        method = http_request['method']
        posts_data = None
        if http_request['post_data']:
            posts_data = http_request['post_data']
        if http_request['use_proxy']:
            use_proxy = http_request['use_proxy']
        else:
            use_proxy = task.parameters['use_proxy']
        if http_request['timeout']:
            timeout = int(http_request['timeout'])
        else:
            timeout = int(task.parameters['timeout'])
        url = http_request['start_url']
        if 'cookies' in task.parameters and task.parameters['cookies']:
            cookies = task.parameters['cookies']
        else:
            cookies = None
        self.logger.info(Colored.green("[Downloader()]: 目前下载URL =>{0}".format(url)))
        retry_times = 0
        max_time = int(http_request['sleep_time'])
        sleep_time = random.uniform(1, max_time)
        max_retry = random.randint(4, 15)
        while retry_times < max_retry:
            proxy = get_random_proxy() if use_proxy else None
            if proxy is not None:
                self.logger.info(Colored.green("[Downloader()]: 目前使用代理 =>{0}".format(proxy)))
            try:
                request = Any
                session = httpx.AsyncClient(proxies=proxy, verify=False)
                if http_request.get('use_session', None) or task.parameters.get('use_session', None):
                    self.session_container.setdefault(task.parameters['spider_name'], session)
                    session = self.session_container.get(task.parameters['spider_name'])
                async with session:
                    if method == GET:
                        request: Coroutine = session.get(
                            url,
                            headers=headers,
                            timeout=timeout,
                            cookies=cookies,
                        )
                    elif method == POST:
                        request: Coroutine = session.post(
                            url,
                            data=posts_data,
                            headers=headers,
                            timeout=timeout,
                            cookies=cookies,
                        )
                    response: Response = await request
                    if response.status_code != httpx.codes.OK:
                        response.raise_for_status()
                    if response is None:
                        return None
                    byte_content: bytes = await response.aread()
                # 返回请求内容
                process_type = http_request['return_type']
                self.logger.info(Colored.green("[Downloader()]: 请求返回类型>>{0}".format(
                    process_type)))
                encoding = chardet.detect(byte_content)['encoding']
                time.sleep(sleep_time)
                if process_type:
                    if process_type == TEXT:
                        return decode_content(byte_content, encoding)
                    elif process_type == JSON:
                        text = decode_content(byte_content, encoding)
                        return json.loads(text)
                    elif process_type == CSS:
                        return bs(byte_content, 'html5lib')
                text = decode_content(byte_content, encoding)
                return etree.HTML(text)
            except Exception as e:
                retry_times += 1
                self.logger.error(Colored.red("[Downloader()]: 目前下载URL =>{0} 重试次数[{1}/{2}] ERROR: {3}".
                                              format(url, retry_times, max_retry, e)), exc_info=True)
                sleep_time *= random.random() * self.sleep_factor
                time.sleep(sleep_time)
        # else:
        #     pass


def store_content(request_dict: Dict, byte_content: bytes) -> None:
    """
    批量储存响应对象
    :param request_dict: 批量响应对象
    :param byte_content: 字节内容
    :return: None
    """
    path = '/tmp/star_crawler'
    create_folder(path)
    token = None
    name = request_dict["url"].split('&r')[0]
    if request_dict["method"] == POST:
        data = request_dict["data"]
        token = generate_token(name, data)
    elif request_dict["method"] == GET:
        token = generate_token(name)
    content = dumps_content(byte_content)
    with open('{0}/{1}'.format(path, token), mode='wb') as f:
        f.write(content)


def load_content(request_dict: Dict) -> Union[None, bytes]:
    """
    加载批量响应对象
    :param request_dict: 批量请求对象
    :return: 批量响应对象
    """
    path = '/tmp/star_crawler'
    create_folder(path)
    token = None
    try:
        name = request_dict["url"].split('&r')[0]
        if request_dict["method"] == POST:
            data = request_dict["data"]
            token = generate_token(name, data)
        elif request_dict["method"] == GET:
            token = generate_token(name)
        if not is_file_exists('{0}/{1}'.format(path, token)):
            return None
        with open('{0}/{1}'.format(path, token), mode='rb') as f:
            buffer = f.read()
        content = loads_content(buffer)
        return content
    except Exception:
        return None
