# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config
import traceback
import requests
from logger import logger
from settings import QINIU_ACCESS_KEY,QINIU_SECRET_KEY,QINIU_BUCKET_NAME


class Retry(object):

    def __init__(self, retry_time=3):
        self.retry_time = retry_time

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            for i in range(self.retry_time):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    traceback.print_exc()
            return False
        return wrapper



class uploader():

    def __init__(self):
        self.access_key = QINIU_ACCESS_KEY
        self.secret_key = QINIU_SECRET_KEY
        self.bucket_name = QINIU_BUCKET_NAME

    @Retry(retry_time=5)
    def upload(self, name, url):
        q = Auth(self.access_key, self.secret_key)
        key = '{}.jpg'.format(name)
        logger.info('start upload')
        #ret, info = put_data(token, key, data)
        bucket = BucketManager(q)
        ret, info = bucket.fetch(url, self.bucket_name, key)
        logger.info(ret)
        logger.info(info)
        if not ret:
            raise Exception('upload data error:{}, {}'.format(name, url))
        logger.info("壁纸上传七牛云成功！原网链接：{}".format(url))
        return ret

if __name__ == '__main__':
    try:
        upl = uploader()
        logger.info(upl.upload('test4', 'http://img5.adesk.com/5fe59ef5e7bce70db57fa97c'))
        logger.info("qiniu upload success!")
    except Exception as e:
        logger.exception(e)


