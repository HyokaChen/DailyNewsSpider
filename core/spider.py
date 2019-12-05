#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 @File       : spider.py
 @Time       : 2019-04-16 21:26
 @Author     : Empty Chan
 @Contact    : chen19941018@gmail.com
 @Description:
 @License    : (C) Copyright 2016-2017, iFuture Corporation Limited.
"""
import sys
import random
import asyncio
import time
import logme
import datetime
from utils.color import Colored
from config.constant import (LEFT_BRACE, RIGHT_BRACE, REQUESTS_TOPIC, PROCESSES_TOPIC, DOT, DOLLAR,
                             RESULTS_TOPIC, TASK_TOPIC, SpiderStatus, AND, WayType, HASH_MAP, AT, HASH,
                             EXCLUDE_FIELD, DIAGONAL, GREATER_THAN, UNDER_LINE, TEMPLATES_TOPIC, COLON)
from core.middleware import TemplateMiddleware, DownloadMiddleware, QueueMiddleware
from core.template import ReadTemplateJson
from core.http import HTTPRequestTemplate, HTTPResultTemplate, HTTPProcessTemplate
from config.constant import PROCESSES, RESULTS, REQUESTS
from core.download import Downloader
from core.queue import TaskQueue, Task
from core.pipeline import ProcessContent
from core import format_data, is_in_range_time, to_dict_2, process_raw_value, sort_time
from utils.format_utils import load_item, load_method
import re
from copy import deepcopy
try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

PARAMETER = re.compile(r'([a-zA-Z_]+[1-9]*)}', re.MULTILINE)


@logme.log(name="[Liz2Bird]")
class Liz2Bird(object):
    """
    利兹与青鸟-爬虫框架
    """
    __slots__ = [
        'templates',
        'download',
        'middlewares',
        'pipeline',
        'queue',
        'spider_status',
        'task_sleep',
    ]

    def __init__(self, dir_path, download: Downloader, pipeline: ProcessContent, queue: TaskQueue):
        """
        初始化函数
        :param dir_path: 处理内容中间结果的函数加载的路径
        :param download: 下载器
        :param pipeline: 内容存放的路径
        :param queue: 任务队列
        """
        self.templates = ReadTemplateJson.read_all_template(dir_path)
        self.middlewares = [TemplateMiddleware(), DownloadMiddleware(),
                            QueueMiddleware()]
        self.download = download
        self.pipeline = pipeline
        self.queue = queue
        self.spider_status = SpiderStatus.Null
        self.task_sleep = 1.5

    def __del__(self):
        """
        析构函数，释放资源
        :return:
        """
        self.logger.info(Colored.yellow("[Liz2Bird]: 释放资源╮(￣▽￣)╭"))
        del self.download

    def run(self, is_master=False):
        """
        启动
        :param is_master: 是否是主节点
        :return:
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._start(is_master))
        except (KeyboardInterrupt, SystemExit):
            tasks = list(asyncio.Task.all_tasks(loop))
            pendings = {t for t in tasks if not t.done()}
            for task in pendings:
                task.cancel()
            loop.run_until_complete(
                asyncio.gather(*pendings, loop=loop, return_exceptions=True))

            for task in pendings:
                if task.cancelled():
                    continue
                if task.exception() is not None:
                    loop.call_exception_handler({
                        'message': 'unhandled exception during asyncio.run() shutdown',
                        'exception': task.exception(),
                        'task': task,
                    })

            if sys.version_info >= (3, 6):  # don't use PY_36 to pass mypy
                loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            self.stop()
            loop.close()
            self.logger.info(Colored.yellow("[Liz2Bird]: Shut down....(@ $ _ $ @)----"))

    async def _start(self, is_master=False):
        """
        开始爬虫
        :param is_master: 是否是主节点
        :return:
        """
        self.logger.info(Colored.green("[Liz2Bird-start()]: Start Spider d=====(￣▽￣*)b"))
        if is_master and self.spider_status == SpiderStatus.Null:
            # 记录 spider 的映射名称
            spiders = []
            global_parameters = []
            # 迭代并提取模板
            for template in self.templates:
                self.logger.info(Colored.green("[Liz2Bird-start()]: 当前读取模板=>{0}".format(template['SPIDER_NAME'])))
                requests, processes, results = self.middlewares[0].middle_origin2engine(template)

                # 所有的 spider 列表
                task_topic = TASK_TOPIC.format(template['SPIDER_NAME'])
                spiders.append(task_topic)
                # spider 对应的全局参数映射，作为后续删除
                global_parameters.append(HASH_MAP.format(template['SITE_NAME']))
                # 放置一些映射关系
                self._queue_push([r.obj2dict() for r in requests], topic=REQUESTS_TOPIC
                                 .format(template['SPIDER_NAME']),
                                 way=WayType.HSET, key_ids=[r.request_id for r in requests])
                self._queue_push([p.obj2dict() for p in processes], topic=PROCESSES_TOPIC
                                 .format(template['SPIDER_NAME']),
                                 way=WayType.HSET, key_ids=[p.process_id for p in processes])
                self._queue_push([r.obj2dict() for r in results], topic=RESULTS_TOPIC
                                 .format(template['SPIDER_NAME']),
                                 way=WayType.HSET, key_ids=[r.result_id for r in results])
                # 如果对应的task spider 没有任务，则先清除旧的 key，然后初始化 task，否则不添加初始 task
                count = self.queue.count(task_topic)
                if count == 0:
                    # 去除全局参数的 key
                    values = self.queue.find(TEMPLATES_TOPIC, way=WayType.HGET, key=task_topic)
                    if values is not None:
                        self_global_parameters_ = self.middlewares[2].middle_origin2engine(*[values])
                        spider = task_topic.split('_')[1]
                        self_global_parameters_ = ['{0}:{1}*'.format(global_parameter, spider) for global_parameter in
                                                   self_global_parameters_]
                        self.queue.delete_all(*self_global_parameters_)
                    # 放入第一个 request 任务
                    one_task = self._build_task(requests[0], template)
                    self._queue_push([one_task])
            # 记录 spider 的映射名称
            self._queue_push(global_parameters,
                             topic=TEMPLATES_TOPIC,
                             key_ids=spiders,
                             way=WayType.HSET)
        # 非 master 节点，进行爬取
        if not is_master:
            try:
                sleep_time = random.uniform(0, 2)
                counter_task = []
                while True:
                    # 弹出 task 并下载
                    total_count, tasks = self._task_pop()
                    if tasks is None or len(tasks) == 0:
                        # 线性增加等待时间
                        sleep_time += self.task_sleep * random.random()
                        self.logger.info(Colored.green("[Liz2Bird-start()]: 无任务，休眠时间 =>{0}".format(sleep_time)))
                        await asyncio.sleep(sleep_time)
                        continue
                    else:
                        sleep_time = random.uniform(0, 2)
                    # 第一个任务
                    task = tasks[0]
                    time.sleep(sleep_time)
                    try:
                        counter_task.append(task)
                        self.logger.info(Colored.green("[Liz2Bird-start()]: 弹出下载ask，task_id>>{0}"
                                                       .format(task.task_id)))
                        download_content_list = await asyncio.gather(*[self._download(t) for t in counter_task],
                                                                     return_exceptions=True)
                        self.logger.info(Colored.green("[Liz2Bird-start()]: 少于 4 个串行请求"))
                        # 处理结果
                        for i, download_content in enumerate(download_content_list):
                            if download_content is None:
                                continue
                            task = counter_task[i]
                            self.logger.info(Colored.green("[Liz2Bird-start()]: 处理Task，采用 process 模板=>{0}"
                                                           .format(task.process_id)))
                            # 处理 task 请求后产生的内容
                            new_task_results = self._process(download_content, task)
                            # next request 的生成
                            next_request_obj = None
                            if task.next_request is not None:
                                self.logger.info(Colored.green("[Liz2Bird-start()]: Next Request，采用 request 模板=>{0}"
                                                               .format(task.next_request)))
                                next_request_bytes = self.queue.find(
                                    REQUESTS_TOPIC.format(task.parameters['spider_name']),
                                    way=WayType.HGET,
                                    key=task.next_request)
                                next_request_template = self.middlewares[2].middle_origin2engine(next_request_bytes)[0]
                                next_request_obj = HTTPRequestTemplate(**next_request_template)
                            # 同一级请求的任务
                            if task.parallel_request is not None:
                                self.logger.info(
                                    Colored.green("[Liz2Bird-start()]: Parallel Request，采用 request 模板=>{0}".format(
                                        task.parallel_request)))
                                parallel_request_bytes = self.queue.find(
                                    REQUESTS_TOPIC.format(task.parameters['spider_name']),
                                    way=WayType.HGET,
                                    key=task.parallel_request)
                                parallel_request_template = \
                                    self.middlewares[2].middle_origin2engine(parallel_request_bytes)[0]
                                parallel_request_obj = HTTPRequestTemplate(**parallel_request_template)
                                new_task = self._build_task(parallel_request_obj, None, pre_task=task,
                                                            result_dict=new_task_results[0])
                                self._queue_push([new_task])
                                if new_task is not None:
                                    self.logger.info(Colored.green(
                                        "[Liz2Bird-start()]: Parallel Task，task_id模板=>{0}".format(new_task['task_id'])))
                            # 下一级请求任务
                            for new_result in new_task_results:
                                # 分类放置处理后的内容
                                if next_request_obj is not None:
                                    new_task = self._build_task(next_request_obj, None, pre_task=task,
                                                                result_dict=new_result)
                                    self._queue_push([new_task])
                                    if new_task is not None:
                                        self.logger.info(Colored.green(
                                            "[Liz2Bird-start()]: 下一个Task，task_id模板=>{0}".format(new_task['task_id'])))
                                else:
                                    self.logger.info(Colored.green("[Liz2Bird-start()]: 生成结果，采用 result 模板=>{0}".format(
                                        task.result_id)))
                                    result = self._build_result(task, result_dict=new_result)
                                    self.pipeline.content_process(result)
                        counter_task.clear()
                    except Exception as e:
                        # 添加任务重试机制
                        task.retry_times += 1
                        if task.retry_times < 5:
                            self._queue_push([task.obj2dict()])
                            self.logger.error(Colored.red("[Liz2Bird-start()]: Task>>>{0}出现错误>>>{1}, 重试次数[{2}/3]...."
                                                          .format(task.task_id, e, task.retry_times)), exc_info=True)
            except Exception as e:
                self.logger.error(Colored.red("[Liz2Bird-start()]: 出现错误>>>{0}....(@ $ _ $ @)----".format(e)),
                                  exc_info=True)
        # 等待关闭
        await self.download.close()

    def stop(self):
        """
        重置爬虫状态，并清除任务队列
        :return:
        """
        self.spider_status = SpiderStatus.Stopping
        self.spider_status = SpiderStatus.Stopped
        # 清除 task 为空的全局参数
        topics = self.queue.find(TEMPLATES_TOPIC, way=WayType.HKEYS)
        topics = [topic.decode('utf-8') for topic in topics]
        for topic in topics:
            count = self.queue.count(topic)
            if count == 0:
                # 去除全局参数的 key
                values = self.queue.find(TEMPLATES_TOPIC, way=WayType.HGET, key=topic)
                if values is not None:
                    global_parameters = self.middlewares[2].middle_origin2engine(*[values])
                    spider = topic.split('_')[1]
                    global_parameters = ['{0}:{1}*'.format(global_parameter, spider)
                                         for global_parameter in global_parameters]
                    self.queue.delete_all(*global_parameters)

    def _build_result(self, task, result_dict):
        """
        构建返回结果对象
        :param task: task
        :param result_dict: 结果字典
        :return: 返回json结果
        """
        current_request = task.request
        return_item = current_request['return_item']
        self.logger.info(Colored.green("[Liz2Bird-_build_result()]: 返回结果匹配的类型=>{0}".format(
            return_item)))
        # 生成item存储
        item_definition = load_item(return_item)
        field_definition = item_definition.get('fields', {})
        item = {"site": task.parameters['site_name'], "data_table": task.parameters['data_table']}
        # item生成
        for field_key, type_value in field_definition.items():
            # item合并metadata数据
            if field_key in result_dict:
                raw_value = result_dict.get(field_key, None)
            else:
                raw_value = task.parameters.get(field_key, None)
            value = process_raw_value(raw_value, type_value)
            item.setdefault(field_key, value)
        if item["url"] == "None":
            item.update({"url": current_request["start_url"]})
        return to_dict_2(item)

    def _build_task(self, request: HTTPRequestTemplate, template=None, pre_task=None, result_dict=None):
        """
        构建 task
        :param request: 请求模板
        :param template: 母模板
        :param pre_task: 前置的 task
        :param result_dict: 结果字典
        :return: task 对象
        """
        # 处理 request 中的未知参数
        parameters = {}
        if template is not None:
            rest_template_fields = {
                key.lower(): template.get(key) for key in template.keys() if key not in [PROCESSES, RESULTS, REQUESTS]
            }
            parameters = rest_template_fields
        task = request.obj2dict()
        if pre_task is not None:
            # 更新 parameters
            parameters.update(pre_task.parameters)
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 更新 pre_task 的参数=>{0}".format(
                pre_task.task_id)))
        # 更新参数组
        if result_dict is not None:
            parameters.update(result_dict)
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 用 result_dict 更新参数"))
        # 第一种情况：start_url 不存在
        if request.start_url is None:
            task['start_url'] = parameters["start_url"]
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 采用起始链接>>>{0}"
                                           .format(parameters["start_url"])))
        # 第二种情况：start_url 是某个 result 模板的解析结果
        elif RESULTS in request.start_url:
            req_url = self._parameter_expression_handler(request.start_url, parameters)
            task['start_url'] = req_url.popitem()[1]
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 采用result 模板{0}，链接为>>{1}"
                                           .format(request.start_url, task['start_url'])))
        # start_url 的参数替换处理
        if request.parameters is not None:
            url_placeholder = self._get_parameters(request.parameters, parameters)
            task['start_url'] = task['start_url'].format(**url_placeholder)
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 更新参数组{0}，链接为>>{1}"
                                           .format(url_placeholder, task['start_url'])))
        # post data 处理
        if request.post_data is not None:
            if not isinstance(request.post_data, dict):
                raise Exception("post data 参数需要时 dict 类型")
            post_data = {}
            for post_data_key, post_data_value in request.post_data.items():
                value = self._parameter_expression_handler(post_data_value, parameters).popitem()[1]
                post_data.setdefault(post_data_key, value)
            task['post_data'] = post_data
        # 处理 referer 的参数处理
        if request.referer is not None and RESULTS in request.referer:
            referer_url = self._parameter_expression_handler(request.referer, parameters)
            task['referer'] = referer_url.popitem()[1]
            self.logger.info(Colored.green("[Liz2Bird-_build_task()]: 采用result 模板{0}，链接为>>{1}"
                                           .format(request.referer, task['referer'])))
        if 'None' in task['start_url']:
            self.logger.error(Colored.red("[Liz2Bird-_build_task()]: URL 中出现 None>>>start_url=>{0}".
                                          format(task['start_url'])))
            return None
        return Task(task_id=None, request=task, parameters=parameters).obj2dict()

    def _queue_push(self, task, topic=None, way=WayType.LPUSH, key_ids=None):
        """
        添加到队列
        :param task: 任务
        :param topic: 主题
        :param way: 方式
        :param key_ids: 键的集合
        :return:
        """
        task = [ta for ta in task if ta is not None]
        if topic is None:
            for ta in task:
                topic = TASK_TOPIC.format(ta['parameters']['spider_name'])
                new_ta = self.middlewares[2].middle_engine2origin(*[ta])
                self.queue.push(topic, new_ta, way=way, key_ids=key_ids)
        else:
            task = self.middlewares[2].middle_engine2origin(*task)
            self.queue.push(topic, task, way=way, key_ids=key_ids)

    def _task_pop(self, count=1):
        """
        task 任务弹出
        :param count: 个数
        :return: task 对象集合
        """
        total_task, topics = self._task_count()
        if total_task < 1:
            return 0, None
        # 返回一个随机的 topic，然后进行 task 的 pop
        topic = random.choice(topics)
        task = self.queue.pop(topic, count)
        if task is None:
            return None
        return total_task, [Task(**t) for t in self.middlewares[2].middle_origin2engine(*task)]

    def _task_count(self):
        """
        task 的个数
        :return: 个数和 topics
        """
        topics = self.queue.find(TEMPLATES_TOPIC, way=WayType.HKEYS)
        topics = [topic.decode('utf-8') for topic in topics]
        total = 0
        want_topics = []
        for topic in topics:
            count = self.queue.count(topic)
            if count == 0:
                continue
            want_topics.append(topic)
            total += count
        return total, want_topics

    async def _download(self, task):
        """
        下载任务
        :param task: task 对象
        :return: 下载结果
        """
        task = self.middlewares[1].middle_engine2origin(task)
        old_content = await self.download.single_download(task)
        return self.middlewares[1].middle_origin2engine(old_content)

    def _process(self, content, task: Task):
        """
        处理下载内容
        :param content: 下载的内容
        :param task: task 任务
        :return: 处理后的结果集合
        """
        if content is None:
            return None
        process_bytes = self.queue.find(PROCESSES_TOPIC.format(task.parameters['spider_name']),
                                        way=WayType.HGET, key=task.process_id)
        processed_content = content
        if task.process_id is not None and process_bytes is None:
            raise Exception('没有找到 process method：{0}！'.format(task.process_id))
        elif process_bytes is not None:
            process_template = self.middlewares[2].middle_origin2engine(process_bytes)[0]
            process_obj = HTTPProcessTemplate(**process_template)
            # 处理 content
            if process_obj.process_method is not None:
                method = load_method(process_obj.process_method)
                if process_obj.parameters is None:
                    processed_content = method(content)
                else:
                    parameters = self._get_parameters(process_obj.parameters, task.parameters)
                    processed_content = method(content, parameters)
        result_bytes = self.queue.find(RESULTS_TOPIC.format(task.parameters['spider_name']),
                                       way=WayType.HGET, key=task.result_id)
        result_template = self.middlewares[2].middle_origin2engine(result_bytes)[0]
        result_obj = HTTPResultTemplate(**result_template)

        self.logger.info(Colored.green("[Liz2Bird-_process()]: 处理的 result 模板>>{0}".format(result_obj.result_id)))
        # 处理 request 中定义的 stopped，默认是位于 range time 的返回内
        stopped = task.request['stopped']
        # 目前支持 page 和range time两种方式
        judge_flag = True if stopped is not None and 'page' in stopped else False
        # range time 的范围
        if HASH in task.parameters['range_time']:
            s_date_str, e_date_str = task.parameters['range_time'].split('#')
        else:
            s_date_str = datetime.datetime.now() - datetime.timedelta(days=1)
            e_date_str = ''
        # 规则匹配内容并返回
        result_dict, result_generator_dict = self._result_template_handler(result_obj, processed_content,
                                                                           task.parameters)
        all_task_result = []
        try:
            if stopped is not None:
                if stopped in result_dict:
                    if judge_flag:
                        # 处理 page 的 stopped
                        page = result_dict.get('page', None)
                        if int(page) > int(result_dict.get(stopped)):
                            return all_task_result
                    elif not is_in_range_time(result_dict.get(stopped), s_date_str, e_date_str):
                        return all_task_result
            if len(result_dict) > 0:
                all_task_result.append(result_dict)
            stopped_list = []
            is_stopped = False
            # 先确定 stopped 停止的字段
            if stopped is not None and stopped in result_generator_dict:
                stopped_value = result_generator_dict.get(stopped)
                # 排序 stopped 字段index
                stopped_args = sort_time(stopped_value)
                del result_generator_dict[stopped]
                for arg in stopped_args:
                    if not is_in_range_time(stopped_value[arg], s_date_str, e_date_str):
                        is_stopped = True
                        break
                    else:
                        stopped_list.append((arg, stopped_value[arg]))
            for key, value in result_generator_dict.items():
                index = 0
                if len(stopped_list) > 0:
                    # 如果 value 小于 stopped_list，则需要填充
                    if 1 == len(value) < len(stopped_list):
                        value = value * len(stopped_list)
                    elif len(value) != len(stopped_list):  # 如果不等于 stopped_list 无法正确填充，故抛出异常
                        raise Exception('key: {0}的 value 值在result_generator_dict中少于 stopped 字段的个数'.format(key))
                    # 如果有停止列表，则按照排序的结果进行选择需要的字段
                    for arg, stopped_val in stopped_list:
                        all_task_result = self._generate_result(key, all_task_result, index,
                                                                value[arg], stopped_val, stopped)
                        index += 1
                else:
                    # 否则，迭代所有的字段，并返回结果
                    for gen_value in value:
                        all_task_result = self._generate_result(key, all_task_result, index,
                                                                gen_value)
                        index += 1
            # 如果没有停止，则把刚才的 request template task 再次扔进去
            if not is_stopped and task.request['is_multiple']:
                current_request_bytes = self.queue.find(REQUESTS_TOPIC.format(task.parameters['spider_name']),
                                                        way=WayType.HGET,
                                                        key=task.request['request_id'])
                current_request_template = self.middlewares[2].middle_origin2engine(current_request_bytes)[0]
                current_request_obj = HTTPRequestTemplate(**current_request_template)
                repeat_task = self._build_task(current_request_obj, None, pre_task=task, result_dict=result_dict)
                self._queue_push([repeat_task])
                self.logger.info(
                    Colored.green("[Liz2Bird-_process()]: repeat task再次放入>>{0}".format(repeat_task['task_id'])))
        except Exception as e:
            self.logger.error(Colored.red("[Liz2Bird-_process()]: 处理出现错误>>>{0}....(@ $ _ $ @)----".format(e)),
                              exc_info=True)
        finally:
            return all_task_result

    @staticmethod
    def _generate_result(key, all_task_result, index, value, stopped_val=None, stopped=None):
        # 判断时间戳
        if len(all_task_result) == 0:
            all_task_result.append({key: value})
        else:
            if key not in all_task_result[0]:
                all_task_result[0].setdefault(key, value)
            # 如果 index 等于目前已有的task result列表长度，说明需要再加入新的 item
            if index == len(all_task_result):
                copy_one = deepcopy(all_task_result[0])
                all_task_result.append(copy_one)
            all_task_result[index].update({key: value})
            if stopped is not None and stopped not in all_task_result[index]:
                # 根据排序时间获得对应的日期
                all_task_result[index].update({stopped: stopped_val})
        return all_task_result

    def _get_parameters(self, parameter_expressions, parameters):
        """
        获取参数
        :param parameter_expressions: 参数模板指定参数来源，可以来自于RESULTS模板，或者本身的字段，也可是list的数组，或者@指定的可变参数
        :return: 参数内容
        """
        # 获取参数模板，可能来自于RESULTS模板，也可能来自于本身的字段
        parameter_from_template = {}
        expressions = parameter_expressions.split(AND)
        for expression in expressions:
            expression = expression.strip()
            temp_results = {}
            from_template = self._parameter_expression_handler(expression, parameters)
            # 如果返回result模板
            if isinstance(from_template, HTTPResultTemplate):
                field_dict = from_template.field_dict
                total_keys = set(field_dict.keys())
                keys = total_keys - EXCLUDE_FIELD
                # 如果不是全局字典，则可以根据RESULTS模板从整体的参数task.parameters获取参数值
                for key in keys:
                    value = parameters.get(key, None)
                    temp_results[key] = value
            # 如果返回数据dict
            elif isinstance(from_template, dict):
                temp_results = from_template
            else:
                raise ValueError('表达式>>{expression} 不被允许, 返回模板:::{result}'.
                                 format(expression=expression, result=from_template))
            self.logger.info(Colored.green('[Liz2Bird-_get_parameters()]:  表达式结果>>>{0}'.format(temp_results)))
            parameter_from_template.update(temp_results)
        return parameter_from_template

    def _result_template_handler(self, result_template, data, parameters):
        """
        结果template的处理
        :param result_template: 结果template
        :param data: 数据
        :return: 结果template的普通映射结果, 以及generator 的映射结果
        """
        temp_results = {}
        temp_generator_results = {}
        temp_parameters = {k: v for k, v in parameters.items()}
        try:
            # 处理result 模板的各个字段
            field_dict = result_template.field_dict
            if result_template.global_parameter is not None and isinstance(result_template.global_parameter, str):
                global_parameters = [p.strip() for p in result_template.global_parameter.split(AND)]
                self.logger.info(Colored.blue("[Liz2Bird-_result_template_handler()]: 全局参数>>>>{0}"
                                              .format(', '.join(global_parameters))))
            else:
                global_parameters = []
            for field, expression in field_dict.items():
                if field in EXCLUDE_FIELD:
                    continue
                self.logger.info(Colored.blue("Liz2Bird-_result_template_handler()]: result 处理字典>>>> (<{0}::{1}>)"
                                              .format(field, expression)))
                # 起始下划线，则直接eval运行
                if field.startswith(UNDER_LINE):
                    expression_result = eval(expression)
                elif isinstance(expression, str):
                    # 起始//采用format_data获得结果
                    if expression.startswith(DIAGONAL):
                        expression_result = format_data(data, expression)
                    # 包含::的 css 提取数据
                    elif COLON in expression:
                        expression_result = format_data(data, expression)
                    # 包含>采用format_data获得结果
                    elif GREATER_THAN in expression:
                        expression_result = format_data(data, expression)
                    # 包含@的正则匹配
                    elif AT in expression:
                        exp, temp_data_field = expression.split(AT)
                        data_field, reg_idx = temp_data_field.split(HASH)
                        temp_data = temp_parameters.get(data_field)
                        if isinstance(temp_data, list):
                            expression_result = []
                            for temp_da in temp_data:
                                expression_one = format_data(temp_da, exp, reg_idx)
                                expression_result.append(expression_one)
                        else:
                            expression_result = format_data(temp_data, exp, reg_idx)
                    # 包含$符号的拼接字段
                    elif expression.startswith(DOLLAR):
                        at_parameters_name = PARAMETER.findall(expression)
                        one_parameters = {}
                        dict_parameter = {}
                        for at_parameter_name in at_parameters_name:
                            parameter_value = temp_parameters.get(at_parameter_name, None)
                            if isinstance(parameter_value, list):
                                dict_parameter.setdefault(at_parameter_name, parameter_value)
                            else:
                                one_parameters.setdefault(at_parameter_name, parameter_value)
                        # 处理 format 表达式
                        extend_parameters_group = []
                        one_round = 0
                        if len(dict_parameter) > 0:
                            for key, value_list in dict_parameter.items():
                                # 扩展参数组
                                for index, value in enumerate(value_list):
                                    if index == one_round:
                                        copy_one = deepcopy(one_parameters)
                                        copy_one.update({key: value})
                                        extend_parameters_group.append(copy_one)
                                        one_round += 1
                                    else:
                                        extend_parameters_group[index].update({key: value})

                        if len(extend_parameters_group) > 0:
                            expression_result = [expression.replace(DOLLAR, "").format(**parameters_group)
                                                 for parameters_group in extend_parameters_group]
                        else:
                            expression_result = expression.replace(DOLLAR, "").format(**one_parameters)
                    elif LEFT_BRACE in expression and RIGHT_BRACE in expression:
                        # 包含{xxx}的参数，进行计算
                        at_parameters_name = PARAMETER.findall(expression)
                        total_parameters = {}
                        for at_parameter_name in at_parameters_name:
                            if at_parameter_name in global_parameters:
                                site = HASH_MAP.format(temp_parameters['site_name'])
                                parameter_value = self.queue.find("{site}:{spider}:{key}"
                                                                  .format(site=site,
                                                                          spider=temp_parameters['spider_name'],
                                                                          key=at_parameter_name),
                                                                  way=WayType.GET, key=at_parameter_name)
                                if isinstance(parameter_value, bytes):
                                    parameter_value = parameter_value.decode('utf-8')
                                total_parameters.setdefault(at_parameter_name, parameter_value)
                            else:
                                parameter_value = temp_parameters.get(at_parameter_name, None)
                            total_parameters.setdefault(at_parameter_name, parameter_value)
                        expression_result = eval(expression.format(**total_parameters))
                    else:
                        # 否则直接返回原结果
                        expression_result = expression
                else:
                    # 否则直接返回原结果
                    expression_result = expression

                # 更新 global 参数
                if field in global_parameters:
                    if isinstance(expression_result, str):
                        expression_result_ = expression_result.encode('utf-8')
                    else:
                        expression_result_ = expression_result
                    site = HASH_MAP.format(temp_parameters['site_name'])
                    self.queue.commit_data("{site}:{spider}:{key}"
                                           .format(site=site,
                                                   spider=temp_parameters['spider_name'],
                                                   key=field),
                                           key=field,
                                           value=expression_result_, way=WayType.SET)
                    self.logger.info(Colored.white("Liz2Bird-_result_template_handler()]: 提交全局参数>>>> (<{0}: {1}>)"
                                                   .format(field, expression_result)))

                # 更新模板结果, result模板字典
                if isinstance(expression_result, list):
                    temp_generator_results.update({field: expression_result})
                else:
                    temp_results.update({field: expression_result})
                temp_parameters.update({field: expression_result})
        except Exception as e:
            self.logger.error(Colored.red("[Liz2Bird-_result_template_handler()]: 出现处理错误>>>{0}....(@ $ _ $ @)----"
                                          .format(e)), exc_info=True)
            raise e
        return temp_results, temp_generator_results

    def _parameter_expression_handler(self, expression, parameters):
        """
        参数表达式处理
        :param expression: 参数表达式
        :return: 参数表达式的结果
        """
        expression_result = {}
        self.logger.info(Colored.blue("[Liz2Bird-_parameter_expression_handler()]: 参数处理模板 =>{0}".format(
            expression)))
        try:
            # 表达式中包含dot
            if DOT in expression and 'http' not in expression:
                left, rights = expression.split(DOT, 1)
                # 包含process处理
                if left == PROCESSES:
                    number = rights[0]
                    process = self.queue.find(PROCESSES_TOPIC.format(parameters['spider_name']),
                                              way=WayType.HGET, key=number)
                    process_template = self.middlewares[2].middle_origin2engine(process)[0]
                    expression_result = HTTPProcessTemplate(**process_template)
                # 包含result处理
                elif left == RESULTS:
                    number, *parameter_name = rights.split(DOT)
                    if len(parameter_name) == 0:
                        result = self.queue.find(RESULTS_TOPIC.format(parameters['spider_name']),
                                                 way=WayType.HGET, key=number)
                        result_template = self.middlewares[2].middle_origin2engine(result)[0]
                        expression_result = HTTPResultTemplate(**result_template)
                    else:
                        value = parameters.get(parameter_name[0], None)
                        expression_result = {parameter_name[0]: value}
                # 包含$处理
                elif left == DOLLAR:
                    parameter_name = rights
                    value = parameters.get(parameter_name, None)
                    expression_result = {parameter_name: value}
            else:
                expression_result = {expression: expression}
        except Exception as e:
            self.logger.error(Colored.red("[Liz2Bird-_parameter_expression_handler()]: 出现处理错误>>>{0}"
                                          .format(e)), exc_info=True)
            raise e
        finally:
            return expression_result
