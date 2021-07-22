#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
from settings import REDIS

redis = redis.Redis(host=REDIS.get("host"), port=REDIS.get("port"))
