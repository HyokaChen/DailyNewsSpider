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
    liz = Liz2Bird('./HotNewsTemplate/CTOLibNewsTemplate.json', Downloader(), RedisProcessContent(), RedisTaskQueue())
    liz.run(is_master=master)


if __name__ == '__main__':
    run()
