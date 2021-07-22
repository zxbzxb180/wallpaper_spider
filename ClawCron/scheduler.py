#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright(c): xiaoliang.chen
# Mail: xlchentj@gmail.com
# Created Time: 2016-06-28 16:02:58

import importlib
import functools
from claw_core.log import logging

# from clients.redis_client import redis
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

timezone_shanghai = timezone("Asia/Shanghai")
logger = logging.getLogger(__name__)


def get_func_by_name(module_name, func_name):
    module = importlib.import_module(module_name)
    return getattr(module, func_name)


class ClawScheduler(object):
    '''DIY Claw Scheduler'''

    def __init__(self, scheduler):
        self.job_lists = {}
        self.scheduler = scheduler

    def register_jobs(self, job_configs):
        for key, jobs in job_configs.items():
            if key == 'interval_jobs':
                self.register_iterval_jobs(jobs)

    def register_iterval_jobs(self, jobs):
        for job in jobs:
            namespaces = job['namespace'].split('.')
            module_name, func_name = '.'.join(namespaces[:-1]), namespaces[-1]
            func = get_func_by_name(module_name, func_name)
            func = self._handler_deco()(func)
            self.__register_interval_job(func, **job['kwargs'])
            self.job_lists[job['namespace']] = func
            logger.info('Regist %s Success!' % (func_name))

    def __register_interval_job(self, job, *args, **kwargs):
        self.scheduler.add_job(job, *args, **kwargs)

    def mget_jobs(self):
        return [key for key in self.job_lists.iterkeys()]

    def run(self):
        self.scheduler.start()

    def state(self):
        return self.scheduler.state

    def _handler_deco(self):
        def outter_wrap(func):
            @functools.wraps(func)
            def inner_wrap(*args, **kwargs):
                try:
                    #namespaces = '.'.join([func.__module__, func.func_name])
                    # 确保同时只有一个定时任务在执行
                    # with redis.lock('lock:claw.cron:{}'.format(namespaces),
                    #                60):
                    ret = func(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                else:
                    return ret
            return inner_wrap
        return outter_wrap

__background_scheduler = BackgroundScheduler(timezone=timezone_shanghai)
scheduler = ClawScheduler(__background_scheduler)
