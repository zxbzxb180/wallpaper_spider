#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE, CalledProcessError
# from clients.redis_client import redis
from claw_core.exc import deco_exc_handler
from claw_core.log import logging
from claw_core.utils import random_string

logger = logging.getLogger(__name__)
current_path = os.path.dirname(os.path.realpath(__file__))
script_path = os.path.realpath(os.path.join(current_path, os.pardir, os.pardir,
                                            os.pardir))

CMD_SUCCESS = 0

"""
# redis lock version

@deco_exc_handler
def timing_tasks(excute_cmd, *args, **kwargs):
    desc = kwargs.get("desc", random_string(4))
    inner_key = 'inner_exclude_job:%s' % desc
    logger.info("inner_key: %s" % inner_key)
    rtn = redis.get(inner_key)
    if not rtn:
        redis.setex(inner_key, 1, 20)
        logger.info("[DEBUG] restart script begin")
        result = subprocess.check_output("cd %s; %s" % (script_path,\
                excute_cmd), shell=True)
        logger.info("excute_ret:{}".format(result))
        redis.delete(inner_key)
        logger.info("release lock : %s" % inner_key)
"""


@deco_exc_handler
def timing_tasks(excute_cmd, *args, **kwargs):
    """
    excute timing_tasks func generalduty
    """
    desc = kwargs.get("desc", "timing_tasks: %s" % random_string(4))
    logger.info("[DEBUG] excute task %s begin" % desc)
    result = check_output("cd %s; %s" \
        % (script_path, excute_cmd), shell=True)
    logger.info("excute_ret:%s" % (result))
    logger.info("excute task %s end\n" % desc)


def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd)
    output = output[:-2] if output.endswith("\n") else output
    return output
