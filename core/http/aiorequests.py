#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : aiorequests.py
 @Time       : 2019-05-11 18:20
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""

import asyncio
import functools

from requests import *


__version__ = "0.1.0"
version = tuple(map(int, __version__.split(".")))


def executor_wrapper(f, *, loop=None, executor=None):
    loop = loop or asyncio.get_event_loop()

    @functools.wraps(f)
    def function_with_async_executor(*args, **kwargs):
        return loop.run_in_executor(executor, functools.partial(f, *args, **kwargs))

    return function_with_async_executor


def set_async_requests(*, loop=None, executor=None):
    setattr(Session, "request", executor_wrapper(Session.request, loop=loop, executor=executor))