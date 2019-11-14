#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : queue.py
 @Time       : 2019-04-16 21:30
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from utils.color import Colored
import json
from hashlib import md5
from utils.db_util import rdb
from utils.bloom_filter import BloomFilter
from config.constant import PROCESSES_DOT, RESULTS_DOT, REQUESTS_DOT, WayType


class Task(object):
    def __init__(self, task_id, request: dict, parameters: dict, retry_times=0):
        self._task_id = task_id
        self._request = request
        self._process_id = None if request['process'] is None else int(request['process'].replace(PROCESSES_DOT, ''))
        self._result_id = int(request['result'].replace(RESULTS_DOT, ''))
        self._next_request = None if request['next_request'] is None else \
            int(request['next_request'].replace(REQUESTS_DOT, ''))
        self._parallel_request = None if request['parallel_request'] is None else \
            int(request['parallel_request'].replace(REQUESTS_DOT, ''))
        self._parameters = parameters
        self._retry_times = retry_times

    @property
    def task_id(self):
        m = md5()
        m.update(self._request['start_url'].encode('utf-8'))
        self._task_id = m.hexdigest()
        return self._task_id

    @property
    def request(self):
        return self._request

    @property
    def process_id(self):
        return self._process_id

    @property
    def result_id(self):
        return self._result_id

    @property
    def next_request(self):
        return self._next_request

    @property
    def parallel_request(self):
        return self._parallel_request

    @property
    def parameters(self):
        return self._parameters

    def obj2dict(self):
        return {
            'task_id': self.task_id,
            'request': self.request,
            'parameters': self.parameters,
            'retry_times': self.retry_times
        }

    @property
    def retry_times(self):
        return self._retry_times

    @retry_times.setter
    def retry_times(self, value):
        self._retry_times = value


class TaskQueue(object):
    def pop(self, topic: str, count=1, way=WayType.RPOP):
        raise NotImplementedError

    def push(self, topic: str, tasks: list, way=WayType.LPUSH, key_ids=None):
        raise NotImplementedError

    def find(self, topic: str, way: WayType, key=None, count=1):
        raise NotImplementedError

    def count(self, topic, way=WayType.LLEN):
        raise NotImplementedError

    def commit_data(self, topic: str, key: str, value, way: WayType):
        raise NotImplementedError

    def delete_all(self, *topics):
        raise NotImplementedError

    def delete(self, topic: str, way: WayType, key=None):
        raise NotImplementedError


class RedisTaskQueue(TaskQueue):
    def __init__(self):
        self.bloom_filter = BloomFilter()

    def pop(self, topic: str, count=1, way=WayType.RPOP):
        pipeline = rdb.pipeline()
        results = []
        if way == WayType.RPOP:
            for _ in range(count):
                pipeline.rpop(topic)
            results = pipeline.execute()
        elif way == WayType.SPOP:
            results = pipeline.spop(topic, count=count)
        return [result for result in results if result is not None]

    def push(self, topic: str, tasks: list, way=WayType.LPUSH, key_ids=None):
        pipeline = rdb.pipeline()
        # 过滤一些任务
        if way == WayType.LPUSH:
            wait_tasks = []
            for task in tasks:
                str_input = json.loads(task, encoding='utf-8')
                is_duplicate = str_input['request']['is_duplicate']
                spider_name = str_input['parameters']['spider_name']
                if is_duplicate:
                    if not self.bloom_filter.is_contains(spider_name, str_input['task_id'].encode('utf-8')):
                        wait_tasks.append(task)
                        self.bloom_filter.insert(spider_name, str_input['task_id'].encode('utf-8'))
                else:
                    wait_tasks.append(task)
            if len(wait_tasks) > 0:
                pipeline.lpush(topic, *wait_tasks)
        elif way == WayType.HSET:
            for i, task in enumerate(tasks):
                pipeline.hset(name=topic, key=key_ids[i], value=task)
        elif way == WayType.SADD:
            pipeline.sadd(topic, *tasks)
        pipeline.execute()

    def find(self, topic: str, way: WayType, key=None, count=1):
        if way == WayType.HGET and key is not None:
            return rdb.hget(name=topic, key=key)
        elif way == WayType.GET:
            return rdb.get(name=topic)
        elif way == WayType.SRANDMEMBER:
            return rdb.srandmember(topic, count)
        elif way == WayType.HKEYS:
            return rdb.hkeys(topic)

    def count(self, topic, way=WayType.LLEN):
        if way == WayType.LLEN:
            return rdb.llen(topic)
        elif way == WayType.SCARD:
            return rdb.scard(topic)
        return 0

    def commit_data(self, topic: str, key: str, value, way: WayType):
        if isinstance(value, dict):
            value = json.dumps(value, ensure_ascii=False)
        if way == WayType.HSET:
            rdb.hset(name=topic, key=key, value=value)
        elif way == WayType.SET:
            rdb.set(name=topic, value=value)

    def delete_all(self, *topics):
        keys = []
        for topic in topics:
            # 匹配正则
            if '*' in topic:
                map_keys = [key.decode('utf-8') for key in rdb.keys(topic)]
                keys.extend(map_keys)
                print(keys)
            else:
                keys.append(topic)
        if len(keys) > 0:
            rdb.delete(*keys)

    def delete(self, topic: str, way: WayType, key=None):
        if way == WayType.HDEL:
            return rdb.hdel(topic, key)