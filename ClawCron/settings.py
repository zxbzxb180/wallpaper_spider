#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright(c): xiaoliang.chen
# Mail: xlchentj@gmail.com
# Created Time: 2016-06-28 15:05:37


# REDIS = {"host": "47.111.74.232", "port": "6379"}
SEEDGENERATOR_HOME = '/home/spider'

# ========== Job Settings ==========

# cron format or settings
# year='*'
# month='*'
# day=1
# week='*',
# day_of_week='*'
# hour='*'
# minute=20
# second=0
#
# Expression    Field    Description
# *               any    Fire on every value
# */a             any    Fire every a values, starting from the import minimum
# a-b             any    Fire on any value within the a-b range (a must be
# smaller than b)  # noqa
# a-b/c           any    Fire every c values within the a-b range
# xth y           day    Fire on the x -th occurrence of weekday y within the
# month  # noqa
# last x          day    Fire on the last occurrence of weekday x within the
# month # noqa
# last            day    Fire on the last day within the month
# x,y,z           any    Fireon any matching expression; can combine any number
# of any of the above expressions  # noqa


JOB_CONFIG = {
    # one job
    'interval_jobs': [
        {
            'namespace': 'tasks.monitoring.timing_tasks',
            'kwargs': {
                'trigger': 'cron',
                'hour': '1',
                'kwargs': {
                    'excute_cmd': 'nohup python wallpaper.py &',
                    'desc': 'wallpaper spider'
                },
            },
            'desc': 'wallpaper spider'
        },
        # {
        #     'namespace': 'tasks.monitoring.timing_tasks',
        #     'kwargs': {
        #         'trigger': 'cron',
        #         'hour': '3',
        #         'kwargs': {
        #             'excute_cmd': 'nohup python auto_upload.py &',
        #             'desc': 'auto upload images to qiniuyun'
        #         },
        #     },
        #     'desc': 'auto upload images to qiniuyun'
        # },
        {
            'namespace': 'tasks.monitoring.timing_tasks',
            'kwargs': {
                'trigger': 'cron',
                'hour': '8',
                'minute': '30',
                'kwargs': {
                    'excute_cmd': 'nohup python daily_wallpaper.py &',
                    'desc': 'daily wallpaper'
                },
            },
            'desc': 'daily wallpaper'
        }
    ]
}
