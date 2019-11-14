#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : sync_to_es.py
 @Time       : 2018/1/20 0020 20:53
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import asyncio
import datetime
import json
import time
import pymongo
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from utils.db_util import mdb, es, INDEX_TEXT, INDEX_MAPPING, create_es_doc
from elasticsearch import helpers

DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


executors = {"default": ThreadPoolExecutor(10), "processpool": ProcessPoolExecutor(2)}
job_defaults = {"coalesce": False, "max_instances": 10}

loop = asyncio.get_event_loop()
scheduler = AsyncIOScheduler(
    {"event_loop": loop}, executors=executors, job_defaults=job_defaults
)
ALL_CATEGORY = ["news"]


# minute
# second
# @scheduler.scheduled_job(trigger='cron', second='*/20', id='sync_to_es')
def sync_to_es():
    collections = mdb.collection_names()
    now = datetime.datetime.now().strftime(DATE_FORMAT)

    # reg = '.*' + now + '.*'
    # reg = '.*2018-02-23.*'
    # for collection in collections:
    #     now_date_news = mdb[collection].find({'insert_time': {'$regex': reg}}, projection={'_id': False})
    #     if not es.indices.exists_type(index=INDEX_TEXT, doc_type=collection):
    #         es.indices.create(index=INDEX_TEXT,
    #                           body=json.loads(INDEX_MAPPING % collection, encoding='utf-8'))
    #     processed = 0
    #     for doc in now_date_news:
    #         try:
    #             print(doc)
    #             json_doc = json.dumps(doc, ensure_ascii=False)
    #             _id = doc.get('id')
    #             es.index(index=INDEX_TEXT, doc_type=collection, body=json_doc, id=_id)
    #             processed += 1
    #             print('Processed: ' + str(processed), flush=True)
    #         except Exception as e:
    #             raise e
    collections = [c for c in collections if "system" not in c]
    # 首先，查看elastic-search的当前type下的最新一条的时间戳
    for category in ALL_CATEGORY:
        for collection in collections:
            # if collection == 'sina':
            #     continue
            create_es_doc(category)
            body = {
                "query": {
                    "query_string": {"default_field": "site", "query": collection}
                },
                "sort": {
                    "insert_time": {"order": "desc"}  # 根据age字段升序排序  # asc升序，desc降序
                },
                "from": 0,
                "size": 1,
            }
            # print(body)
            last_news_hits = es.search(index=INDEX_TEXT, doc_type=category, body=body)[
                "hits"
            ]["hits"]
            print("{0}==>last_news_hits".format(len(last_news_hits)))
            if len(last_news_hits) > 0:
                last_news = last_news_hits[0]["_source"]
                # print(last_news)
                # now_date_news = mdb[collection].find({'timestamp':  {'$gt': last_news['timestamp']}},
                #                                      projection={'_id': False}).sort('field', pymongo.ASCENDING)
                pipeline = [
                    {"$match": {"timestamp": {"$gte": last_news["timestamp"]}}},
                    {"$sort": {"timestamp": pymongo.ASCENDING}},
                    {"$limit": 300},
                ]
                now_date_news = mdb[collection].aggregate(pipeline, allowDiskUse=True)
                _actions = []
                # i = 0
                for news in now_date_news:
                    # print(news)
                    if (
                        str(news.get("timestamp")).strip()
                        == str(last_news["timestamp"]).strip()
                    ):
                        print("skip")
                        continue
                    _id = news.get("_id")
                    print(_id)
                    del news["_id"]
                    json_doc = json.dumps(news, ensure_ascii=False)
                    action = {
                        "_index": INDEX_TEXT,
                        "_type": category,
                        "_id": _id,
                        "_source": json_doc,
                    }
                    _actions.append(action)
                    # es.index(index=INDEX_TEXT, doc_type=collection, body=json_doc, id=_id)
                try:
                    state, _ = helpers.bulk(
                        es, _actions, stats_only=False, raise_on_error=True
                    )
                    print("all news synchronous {state} !!!".format(state=state))
                    print("all news synchronous {state} !!!".format(state=state))
                except Exception as e:
                    raise e
            else:
                pipeline = [
                    {"$sort": {"timestamp": pymongo.ASCENDING}},
                    {"$limit": 500},
                ]
                all_news = mdb[collection].aggregate(pipeline, allowDiskUse=True)
                _actions = []
                for news in all_news:
                    # print('-------')
                    # print(news)
                    _id = news.get("_id")
                    print(_id)
                    del news["_id"]
                    json_doc = json.dumps(news, ensure_ascii=False)
                    action = {
                        "_index": INDEX_TEXT,
                        "_type": category,
                        "_id": _id,
                        "_source": json_doc,
                    }
                    _actions.append(action)
                    # es.index(index=INDEX_TEXT, doc_type=collection, body=json_doc, id=_id)
                try:
                    state, _ = helpers.bulk(
                        es, _actions, stats_only=False, raise_on_error=True
                    )
                    print("all news synchronous {state} !!!".format(state=state))
                except Exception as e:
                    raise e

    print("{now} all news synchronous!".format(now=now))


if __name__ == "__main__":
    while True:
        sync_to_es()
        time.sleep(20)
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()
    # print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    #
    # # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    # try:
    #     loop.run_forever()  # 保证事件loop运行
    # except (KeyboardInterrupt, SystemExit):
    #     exit(0) # projection={'_id': False}
    # all_news = mdb['tencent'].find().sort('timestamp', pymongo.ASCENDING)
    # _actions = []
    # for news in all_news:
    #     try:
    #         print('-------')
    #         print(news)
    #         _id = news.get('_id')
    #         del news['_id']
    #         json_doc = json.dumps(news, ensure_ascii=False)
    #         action = {
    #             "_index": INDEX_TEXT,
    #             "_type": 'tencent',
    #             "_id": _id,
    #             "_source": json_doc
    #         }
    #         print(action)
    #         # es.index(index=INDEX_TEXT, doc_type=collection, body=json_doc, id=_id)
    #     except Exception as e:
    #         raise e

"""
db.createUser({
    user:"spider",
    pwd:"spider_",
    roles:[
        {
            role:"userAdminAnyDatabase",
            db:"admin"
        }
    ]
})

db.createUser({
    user:"star",
    pwd:"StAr@2019Kn0w",
    roles:[
        {
            role:"readWrite",
            db:"data_db"
        }
    ]
})
"""