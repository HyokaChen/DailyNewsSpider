#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : es_utils.py
 @Time       : 2018/4/15 0015 21:13
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json
from elasticsearch import Elasticsearch

# from gevent import monkey
# monkey.patch_all()
from elasticsearch import helpers

es = Elasticsearch(
    [
        {"host": "school-pc", "port": 9200, "timeout": 15000},
        {"host": "school-pc", "port": 9201, "timeout": 15000},
    ],
    http_auth=("elastic", "spider_"),
)

INDEX_TEXT = "news-text"
DOC_TYPE = "news"
INDEX_MAPPING = {
    "news": (
        """{"mappings": {"news": {"properties": {
                    "insert_time": {
                        "type": "date"
                    },
                    "url": {
                        "type": "text"
                    },
                    "news_time": {
                        "type": "date"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    },
                    "news_comments": {
                        "type": "nested",
                        "properties": {
                            "comment": {
                                "type": "text",
                                "analyzer": "ik_max_word",
                                "search_analyzer": "ik_max_word"
                            },
                            "reply": {
                                "type": "text",
                                "analyzer": "ik_max_word",
                                "search_analyzer": "ik_max_word"
                            }
                        }
                    },
                    "timestamp": {
                        "type": "float"
                    },
                    "site": {
                        "type": "text",
                        "analyzer": "ik_max_word",
                        "search_analyzer": "ik_max_word"
                    }
                }
            }
        }
    }"""
    )
}


def delete_es_doc(doc_id, doc_type="news"):
    es.delete(index=INDEX_TEXT, doc_type=doc_type, id=doc_id)


def delete_es_query(query, doc_type="news"):
    es.delete_by_query(index=INDEX_TEXT, body=query, doc_type=doc_type)


def update_es_doc(doc_id, doc_type="news"):
    es.update(index=INDEX_TEXT, body={}, doc_type=doc_type, id=doc_id)


def update_es_query(query, doc_type="news"):
    es.update_by_query(index=INDEX_TEXT, body=query, doc_type=doc_type)


if __name__ == "__main__":
    quety = {
        "script": 'ctx._source.site = "sina"',
        "query": {
            "bool": {
                "must": [{"query_string": {"default_field": "site", "query": "news"}}],
                "must_not": [],
                "should": [],
            }
        },
    }
    update_es_query(quety)
