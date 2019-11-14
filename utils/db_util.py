#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : db_util.py
 @Time       : 2019-04-16 21:45
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
# from gevent import monkey
# monkey.patch_all()
from pymongo import MongoClient
import redis
# from elasticsearch import Elasticsearch
from config.constant import (MONGODB_HOST, MONGODB_PORT, REDIS_PWD,
                             MONGODB_PWD, MONGODB_USER, REDIS_HOST, REDIS_PORT
                             )

pool = redis.ConnectionPool(max_connections=5000, host=REDIS_HOST, port=REDIS_PORT, socket_timeout=10,
                            retry_on_timeout=10, password=REDIS_PWD, db=0)
rdb = redis.StrictRedis(connection_pool=pool)
rdb_publish = redis.StrictRedis().from_url("redis://:{0}@{1}:{2}/3".format(
    REDIS_PWD, REDIS_HOST, REDIS_PORT
))

client = MongoClient(host=MONGODB_HOST, port=MONGODB_PORT)
if MONGODB_USER != '':
    client.data_db.authenticate(MONGODB_USER, MONGODB_PWD, mechanism='SCRAM-SHA-1')
mdb = client.data_db

# es = Elasticsearch([{"host": "school-pc", "port": 9200, "timeout": 15000},
#                     {"host": "school-pc", "port": 9201, "timeout": 15000}], http_auth=('elastic', 'spider_'))


# INDEX_TEXT = 'news-text-v1'
# DOC_TYPE = "news"
# INDEX_MAPPING = {"news":
#                      ('''{"mappings": {"news": {"properties": {
#                     "insert_time": {
#                         "type": "date"
#                     },
#                     "url": {
#                         "type": "text"
#                     },
#                     "news_time": {
#                         "type": "date"
#                     },
#                     "title": {
#                         "type": "text",
#                         "analyzer": "ik_max_word",
#                         "search_analyzer": "ik_max_word"
#                     },
#                     "content": {
#                         "type": "text",
#                         "analyzer": "ik_max_word",
#                         "search_analyzer": "ik_max_word"
#                     },
#                     "news_comments": {
#                         "type": "nested",
#                         "properties": {
#                             "comment": {
#                                 "type": "text",
#                                 "analyzer": "ik_max_word",
#                                 "search_analyzer": "ik_max_word"
#                             },
#                             "reply": {
#                                 "type": "text",
#                                 "analyzer": "ik_max_word",
#                                 "search_analyzer": "ik_max_word"
#                             }
#                         }
#                     },
#                     "timestamp": {
#                         "type": "float"
#                     },
#                     "site": {
#                         "type": "text",
#                         "analyzer": "ik_max_word",
#                         "search_analyzer": "ik_max_word"
#                     }
#                 }
#             }
#         }
#     }''')
#                  }


def mongo_map(name):
    """
    mongo db的映射
    :param name: 创建的mongo集合名称
    :return: mongo集合，类似于表格
    """
    return eval('mdb.{0}'.format(name))


def find_data(collection, name):
    pipeline = [
        {"$match": {'name': name}},
        {"$limit": 1},
    ]
    items = mdb[collection].aggregate(pipeline, allowDiskUse=True)
    for item in items:
        return item
    else:
        return None


def insert_data(collection, data):
    _id = data.get('_id', None)
    if not _id:
        raise Exception('data not have _id field!!')
    if not mdb[collection].find_one({'_id': _id}):
        mdb[collection].insert_one(data)
        return True
    return False


# def create_es_doc(doc_type):
#     if not es.indices.exists_type(index=INDEX_TEXT, doc_type=doc_type):
#         es.indices.create(index=INDEX_TEXT,
#                           body=json.loads(INDEX_MAPPING[doc_type], encoding='utf-8'))


if __name__ == '__main__':
    # mongo_map('cjh').insert_one({'ssss': 123})
    # es.indices.create(index='news-text', body=json.loads(INDEX_MAPPING.format(doc_type='tencent'), encoding='utf-8'))
    # import json
    # text = INDEX_MAPPING % "tencent"
    # print(text)
    # di = json.loads(text, encoding='utf-8')
    # print(di)
    # create_es_doc()
    pass