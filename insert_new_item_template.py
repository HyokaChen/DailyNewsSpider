#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : insert_new_item_template.py
 @Time       : 2019-05-19 14:54
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import datetime
import time
from utils.db_util import insert_data
# 插入item 定义
if __name__ == '__main__':
    # news 定义
    news_item = {
        "_id": "news_item",
        "name": "NewsItem",
        "fields": {
            "url": "str",
            "title": "str",
            "content": "str",
            "news_time": "str",
            "site": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # star 定义
    # 1: 白羊， 2：金牛，3：双子，4：巨蟹，5：狮子，6：处女，7：天秤，
    # 8：天蝎，9：射手，10：摩羯，11：水瓶，12：双鱼
    star_item = {
        "_id": "star_item",
        "name": "StarItem",
        "fields": {
            "url": "str",
            "name": "str",
            "pic": "str",
            "gender": "str",
            "birth_year": "str",
            "birth_month": "str",
            "birth_day": "str",
            "height": "str",
            "astrology": "str",  # 星座1,2,3,4,5,6,7,8,9,10,11,12
            "nationality": "str",  # 国籍 1:
            "profession": "str",
            "base": "str",
            "intro": "str",
            "achievement": "str",
            "event": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # # movie 定义
    # movie_item = {
    #     "_id": "movie_item",
    #     "name": "MovieItem",
    #     "fields": {
    #         "url": "str",
    #         "title": "str",
    #         "pic": "str",
    #         "alias_title": "str",
    #         "score": "str",
    #         "director": "str",
    #         "star": "str",
    #         "type": "str",
    #         "category": "str",
    #         "screen_time": "str",
    #         "nationality": "str",
    #         "video_length": "str",
    #         "base": "str",
    #         "plot": "str"
    #     },
    #     "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    #     "timestamp": time.time()
    # }
    # # tv 定义
    # tv_item = {
    #     "_id": "tv_item",
    #     "name": "TvItem",
    #     "fields": {
    #         "url": "str",
    #         "title": "str",
    #         "pic": "str",
    #         "alias_title": "str",
    #         "score": "str",
    #         "director": "str",
    #         "star": "str",
    #         "type": "str",
    #         "screen_time": "str",
    #         "nationality": "str",
    #         "category": "str",
    #         "base": "str",
    #         "plot": "str"
    #     },
    #     "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    #     "timestamp": time.time()
    # }
    # media 定义
    media_item = {
        "_id": "media_item",
        "name": "MediaItem",
        "fields": {
            "url": "str",
            "title": "str",
            "pic": "str",
            "alias_title": "str",
            "score": "str",
            "director": "str",
            "star": "str",
            "type": "list",
            "category": "str",
            "screen_time": "str",
            "nationality": "list",
            "video_length": "str",
            "base": "str",
            "plot": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # # gov land
    # gov_land_item = {
    #     "_id": "gov_land_item",
    #     "name": "GovLandItem",
    #     "fields": {
    #         "url": "str",
    #         "title": "str",
    #         "index": "str",
    #         "open_way": "str",
    #         "open_date": "str",
    #         "number": "str",
    #         "unit": "str",
    #         "category": "str",
    #         "content": "str"
    #     }
    # }
    # hot news 定义
    hot_item = {
        "_id": "hot_news_item",
        "name": "HotNewsItem",
        "fields": {
            "url": "str",
            "title": "str",
            "author": "str",
            "description": "str",
            "content": "str",
            "news_time": "str",
            "site": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # finish novel
    novel_item = {
        "_id": "finish_novel_item",
        "name": "FinishNovelItem",
        "fields": {
            "url": "str",
            "title": "str",
            "author": "str",
            "tags": "str",
            "intro": "str",
            "count": "str",
            "site": "str",
            "status": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # paper
    paper_item = {
        "_id": "paper_item",
        "name": "PaperItem",
        "fields": {
            "url": "str",
            "title": "str",
            "author": "str",
            "description": "str",
            "tags": "str",
            "site": "str",
            "code": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    # image
    image_item = {
        "_id": "image_item",
        "name": "ImageItem",
        "fields": {
            "url": "str",
            "site": "str"
        },
        "last_modified": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "timestamp": time.time()
    }
    insert_data('items', image_item)