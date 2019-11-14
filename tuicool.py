#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : main.py
 @Time       : 2019-05-06 21:53
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import click
from core.spider import Liz2Bird
from core.download import Downloader
from core.pipeline import RedisProcessContent
from core.queue import RedisTaskQueue


@click.command()
@click.option("--master", "-m", default=False)
@click.option("--path", "-p", default="./", type=str)
def run(master, path):
    liz = Liz2Bird('./HotNewsTemplate/TuicoolNewsTemplate.json', Downloader(cookies={"_tuicool_session":
                                                                                         "BAh7CUkiD3Nlc3Npb25faWQGOgZFVEkiJTBkNmI3NTg4OTYwYTY3Y2I2Nzc5NDhiMWMwOTU1OWRjBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMVlCc1NmbjVvQ3pXT3YxNG1DYWJkN25rUmNPY0NlUjlSRk9zajI1WEk2clk9BjsARkkiDHVzZXJfaWQGOwBGaQNVLAFJIg5yZXR1cm5fdG8GOwBGSSItaHR0cHM6Ly93d3cudHVpY29vbC5jb20vYXJ0aWNsZXMvQk5Ccm1tSQY7AFQ%3D--d06846d78f7a6ff138df8eae3d06417a66703a24"}), RedisProcessContent(), RedisTaskQueue())
    liz.run(is_master=master)


if __name__ == '__main__':
    run()
