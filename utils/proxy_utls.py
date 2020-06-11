#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : proxy_utls.py
 @Time       : 2017/12/2 0002 19:46
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import json
import requests
import random
from utils.decorator import safely_json_loads
from utils.db_util import rdb
from utils import UserAgent
import random
ua = UserAgent()


def get_random_proxy():
    result = {
        'http': 'http://127.0.0.1:1087',
        'https': 'http://127.0.0.1:1087'
    }
    return result

# async def get_random_proxy():
#     session = aiorequests.session()
#     random_proxy = rdb.spop("proxy_cached")
#     if random_proxy:
#         temp = safely_json_loads(random_proxy)
#         print(temp)
#         return {
#             "http": "{ip}:{port}".format(ip=temp.get("ip"), port=temp.get("port")),
#             "https": "{ip}:{port}".format(ip=temp.get("ip"), port=temp.get("port")),
#         }
#     proxy_json = await session.get(
#         "http://www.xdaili.cn/ipagent//freeip/getFreeIps?page=1&rows=10",
#         headers={"Referer": "http://www.xdaili.cn/freeproxy", "User-Agent": ua.random},
#     )
#     rows = proxy_json.json()
#     rows = rows.get("RESULT").get("rows")
#     for row in rows:
#         rdb.sadd("proxy_cached", json.dumps(row, ensure_ascii=False))
#     num = random.randint(0, len(rows) - 1)
#     # print(rows[num])
#     proxy = {
#         "http": "{ip}:{port}".format(
#             ip=rows[num].get("ip"), port=rows[num].get("port")
#         ),
#         "https": "{ip}:{port}".format(
#             ip=rows[num].get("ip"), port=rows[num].get("port")
#         ),
#     }
#     session.close()
#     return proxy


if __name__ == "__main__":
    proxy = get_random_proxy()
    print(proxy)
