#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : middleware.py
 @Time       : 2019-04-18 20:52
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
from core.http import HTTPRequestTemplate, HTTPResultTemplate, HTTPProcessTemplate
from config.constant import REQUESTS, RESULTS, PROCESSES
import json


class Middleware(object):
    def middle_origin2engine(self, *obj):
        """
        从源头发往引擎
        :param obj:
        :return:
        """
        raise NotImplementedError

    def middle_engine2origin(self, *obj):
        """
        从引擎发往源头
        :param obj:
        :return:
        """
        raise NotImplementedError


class TemplateMiddleware(Middleware):
    def middle_origin2engine(self, *obj):
        template = obj[0]
        # 请求template集合
        request_templates = [HTTPRequestTemplate(**request_template)
                             for request_template in template.get(REQUESTS)]
        # 处理template集合
        process_templates = [HTTPProcessTemplate(**process_template)
                             for process_template in template.get(PROCESSES)]
        result_templates = []
        # 结果template集合
        for result_template in template.get(RESULTS):
            result_id = result_template.get('result_id')
            global_parameter = result_template.get('global_parameter', None)
            temp_data = result_template
            del temp_data['result_id']
            if 'global_parameter' in temp_data:
                del temp_data['global_parameter']
            result = HTTPResultTemplate(result_id=result_id,
                                        field_dict=temp_data,
                                        global_parameter=global_parameter,
                                        )
            result_templates.append(result)
        request_templates.sort(key=lambda item: item.request_id)
        process_templates.sort(key=lambda item: item.process_id)
        result_templates.sort(key=lambda item: item.result_id)
        return request_templates, process_templates, result_templates

    def middle_engine2origin(self, *obj):
        pass


class DownloadMiddleware(Middleware):
    def middle_origin2engine(self, *obj):
        return obj[0]

    def middle_engine2origin(self, *obj):
        return obj[0]


class QueueMiddleware(Middleware):
    def middle_origin2engine(self, *obj):
        return [json.loads(o, encoding='utf-8') for o in obj]

    def middle_engine2origin(self, *obj):
        return [json.dumps(o, ensure_ascii=False) for o in obj]