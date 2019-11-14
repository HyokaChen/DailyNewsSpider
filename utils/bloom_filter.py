#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : bloom_filter.py
 @Time       : 2019-04-16 21:44
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import redis
import mmh3
from hashlib import md5
from config.constant import REDIS_HOST, REDIS_PORT, REDIS_PWD


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = mmh3.hash(value, self.seed)
        return abs(ret) % self.cap


class BloomFilter(object):
    def __init__(self, block_num=3):
        """
        :param block_num: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        """
        pool = redis.ConnectionPool(max_connections=5000, host=REDIS_HOST,
                                    port=REDIS_PORT, db=1,
                                    socket_timeout=10,
                                    retry_on_timeout=10,
                                    password=REDIS_PWD)
        self.server = redis.StrictRedis(connection_pool=pool)
        self.bit_size = 1 << 30  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.blockNum = block_num
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, key, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, key, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


# if __name__ == '__main__':
#     bf1 = BloomFilter(key='test1')
#     bf2 = BloomFilter(key='test2')
#     bf3 = BloomFilter(key='test3')
#     bf4 = BloomFilter(key='test4')
#     bf1.insert('http://www.baidu.com')
#     bf2.insert('http://www.baidu.com')
#     bf3.insert('http://www.baidu.com')
#     bf4.insert('http://www.baidu.com')
#
#     print bf1.server.keys()
#     bf1.clear()
#     print bf1.server.keys()
#     bf2.clear()
#     print bf1.server.keys()
#     bf3.clear()
#     print bf1.server.keys()
#     bf4.clear()
#     print bf1.server.keys()