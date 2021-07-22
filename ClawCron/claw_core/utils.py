#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import string


def random_number(length):
    assert length > 0
    return random.randrange(10 ** (length - 1), 10 ** length)


def random_string(length):
    assert length > 0
    return ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" + '0123456789')
                   for x in range(length))

