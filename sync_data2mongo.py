#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : sync_data2mongo.py
 @Time       : 2019-05-11 23:06
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from config.constant import STORE_TOPIC, AT, PUBLISHED
from utils.color import Colored
from utils.db_util import rdb, insert_data, rdb_publish
import logme
import json
import random
import time


@logme.log(name="Data2MongoDB")
def sync_data2mongodb(logger=None):
    logger.info(Colored.green("[Data2MongoDB]: 正在从 redis 同步数据到 mongodb----"))
    items = rdb.spop(STORE_TOPIC, count=500)
    index = 0
    wait_publish_ids = []
    for item in items:
        try:
            json_dict = json.loads(item, encoding='utf-8')
            collection = json_dict.get('data_table', "").split(AT)[1]
            del json_dict['data_table']
            _id = json_dict['_id']
            if _id == '1d33c55f57dd60237f2657028814b638':
                continue
            if insert_data(collection, json_dict):
                logger.info(Colored.blue("[Data2MongoDB]: db:{1} >> content 的 id==>{0}".format(json_dict.get('_id'),
                                                                                               collection)
                                         ))
                wait_publish_ids.append((PUBLISHED.format(collection), json_dict['_id']))
                index += 1
        except Exception as e:
            rdb.sadd(STORE_TOPIC, item)
            logger.error(Colored.red("[Data2MongoDB]: 发生错误>>>{0},"
                                     .format(e)), exc_info=True)
    try:
        pipeline = rdb_publish.pipeline(transaction=False)
        for key, value in wait_publish_ids:
            pipeline.sadd(key, value)
        pipeline.execute()
    except Exception as e:
        logger.error(Colored.red("[Data2MongoDB]: 推送到 redis 发生错误>>>{0},"
                                 .format(e)), exc_info=True)
    logger.info(Colored.blue("[Data2MongoDB]: 当前轮次共同步条数==>{0}".format(index)))


if __name__ == '__main__':
    times = 1.5
    sleep_time = 180
    while True:
        try:
            sync_data2mongodb()
            sleep_time = 180
            print('休眠180秒~~~~~~')
            time.sleep(sleep_time)
        except Exception as e:
            sleep_time += times * random.uniform(3, 6)
            time.sleep(sleep_time)
            print(e)
