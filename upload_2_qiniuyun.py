# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag, put_data, BucketManager
import qiniu.config
import traceback
import requests
from utils.my_requests import retry_requests, get_proxies
from logger import logger

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
        self.access_key = 'y7k-joOhrEX-qsurh6pUNh6w5A6IanC2SfdsiJ4k'
        self.secret_key = 'c-vtkVrzHjCTYxOZMDWT-fX6oH6KnCdB_q9ynLDx'
        self.bucket_name = 'chenxi-img'

    @Retry(retry_time=5)
    def upload(self, name, url):
        q = Auth(self.access_key, self.secret_key)
        key = '{}.jpg'.format(name)
        #token = q.upload_token(self.bucket_name, key, 7200)
        #headers = {
        #        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
        #        }
        #resp = retry_requests(url, headers=headers, stream=True)
        #if resp and resp.status_code == 200:
        #    data = resp.content
        #    if len(data) < 1024 * 100:
        #        raise Exception('too small image')
        #else:
        #    print(resp.status_code)
        #    raise Exception('not resp error')
        logger.info('start upload')
        #ret, info = put_data(token, key, data)
        bucket = BucketManager(q)
        ret, info = bucket.fetch(url, self.bucket_name, key)
        logger.info(ret)
        logger.info(info)
        if not ret:
            raise Exception('upload data error:{}'.format(url))
        logger.info("壁纸上传七牛云成功！壁纸链接：{}".format(url))
        return ret

if __name__ == '__main__':
    try:
        upl = uploader()
        logger.info(upl.upload('test4', 'http://img5.adesk.com/5fe59ef5e7bce70db57fa97c'))
        logger.info("qiniu upload success!")
    except Exception as e:
        logger.exception(e)


