#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright(c): xiaoliang.chen
# Mail: xlchentj@gmail.com
# Created Time: 2016-06-28 14:58:48

import os
import sys
import time
from claw_core.log import logging
from settings import JOB_CONFIG
from scheduler import scheduler

_file_path = os.path.realpath(os.path.dirname(__file__))
sys.path.append(_file_path)
os.environ['PYTHON_EGG_CACHE'] = _file_path

logger = logging.getLogger(__name__)
scheduler.register_jobs(JOB_CONFIG)


class Dispatcher(object):
    def __init__(self):
        logger.info('claw.cron service start!')

    def run(self):
        scheduler.run()
        while True:
            time.sleep(60 * 60)
            # logger.info("claw_scheduler state: {}".format(scheduler.state()))

if __name__ == "__main__":
    service = Dispatcher()
    service.run()
