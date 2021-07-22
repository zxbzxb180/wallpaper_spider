#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from logging import handlers

FORMATTER = '%(asctime)s %(filename)s [line:%(lineno)d] [%(levelname)s]: %(message)s'  # noqa
LOG_FILES = ["./logs/claw_cron.log", "./logs/claw_cron.err"]

logging.basicConfig(level=logging.DEBUG,
                    format=FORMATTER,
                    # datefmt='%Y-%m-%d %H:%M:%S,%f',
                    filename=LOG_FILES[0], \
                    filemode='w')

err_handler = logging.FileHandler(LOG_FILES[1], 'w')
err_handler.setLevel(logging.ERROR)
err_handler.setFormatter(logging.Formatter(FORMATTER))
logging.getLogger().addHandler(err_handler)


for file in LOG_FILES:
    day_handler = handlers.\
        TimedRotatingFileHandler(file, 'MIDNIGHT', 1, 5)
    if LOG_FILES.index(file):
        day_handler.setLevel(logging.ERROR)
    else:
        day_handler.setLevel(logging.INFO)
    day_handler.setFormatter(logging.Formatter(FORMATTER))
    logging.getLogger().addHandler(day_handler)

