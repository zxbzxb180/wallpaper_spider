# -*- coding: utf-8 -*-
from qiniu import Auth, put_file, etag
import qiniu.config

access_key = 'y7k-joOhrEX-qsurh6pUNh6w5A6IanC2SfdsiJ4k'
secret_key = 'c-vtkVrzHjCTYxOZMDWT-fX6oH6KnCdB_q9ynLDx'
q = Auth(access_key, secret_key)
bucket_name = 'chenxi-img'
key = 'test.jpg'
#上传文件到存储后， 存储服务将文件名和文件大小回调给业务服务器。
policy={
         'callbackUrl':'http://your.domain.com/callback.php',
          'callbackBody':'filename=$(fname)&filesize=$(fsize)'
           }
token = q.upload_token(bucket_name, key, 3600)
localfile = './test.jpg'
ret, info = put_file(token, key, localfile)
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
