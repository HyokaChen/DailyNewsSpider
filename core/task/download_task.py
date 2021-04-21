#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : download_task.py
 @Time       : 2020/3/27 22:36
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2020, iFuture Corporation Limited.
"""
import time
from config.constant import StatusType


class DownloadTask(object):
    """
    下载任务实体类
    """
    def __init__(self, task_name: str, download_url: str,
                 status: StatusType,
                 pre_task_id: str, retry_times: int = 0,
                 extra_data: dict = None):
        """
        初始化
        :param task_name: 任务名称
        :param download_url: 下载链接
        :param status: 状态
        :param pre_task_id: 前置任务 id
        :param retry_times: 任务重试次数
        :param extra_data: 额外数据
        :return
        """
        self._task_id = f"{task_name}-{str(time.time()) * 1000}"
        self._download_url = download_url
        self._status = status
        self._pre_task_id = pre_task_id
        self._retry_times = retry_times
        self._extra_data = extra_data

    @property
    def task_id(self):
        """
        任务 id 号
        :param self
        :return 任务 id
        """
        return self._task_id

    @property
    def pre_task_id(self):
        """
        前置任务 id 号
        :param self
        :return 前置任务 id
        """
        return self._pre_task_id

    @property
    def status(self):
        """
        任务状态
        :param self
        :return 任务 id
        """
        return self._status

    @status.setter
    def status(self, value: StatusType):
        """
        设置任务状态
        :param self
        :param value: 更新的状态
        :return
        """
        self._status = value

    @property
    def retry_times(self):
        """
        重试次数
        :param self
        :return 重试次数
        """
        return self._retry_times

    @retry_times.setter
    def retry_times(self, value: int):
        """
        设置任务重试次数
        :param self
        :param value: 新增次数
        :return
        """
        self._retry_times += value

    @property
    def extra_data(self):
        """
        任务额外数据
        :param self
        :return 额外数据
        """
        return self._extra_data

    @extra_data.setter
    def extra_data(self, value: dict):
        """
        设置任务额外数据
        :param self
        :param value: 更新的额外数据
        :return
        """
        self._extra_data.update(value)

    def __str__(self):
        return {
            'task_id': self._task_id,
            'download_url': self._download_url,
            'status': self._status,
            'pre_task_id': self._pre_task_id,
            'retry_times': self._retry_times,
            'extra_data': self._extra_data
        }
    __repr__ = __str__
