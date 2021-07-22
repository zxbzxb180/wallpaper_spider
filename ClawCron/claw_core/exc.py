#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
#from log import logging
from functools import wraps

#logger = logging.getLogger(__name__)


def deco_exc_handler(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            #logger.error(traceback.format_exc())
            #logger.error(str(e))
            print(traceback.format_exc())
    return wrap
