import pymongo
import pymysql

import traceback
import hashlib
from datetime import datetime

from upload_2_qiniuyun import uploader

from logger import logger
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MONGO_HOST, MONGO_PORT, HANDLE_LIST, MONGO_USERNAME, MONGO_PASSWORD, MONGO_AUTH_SOURCE, MONGO_AUTH_MECHANISM

from utils.uid import get_uid

class AutoUploader():

    def __init__(self):
        self.sql_client = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8')
        logger.info("连接mysql数据库成功")
        self.client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD, authSource=MONGO_AUTH_SOURCE, authMechanism=MONGO_AUTH_MECHANISM)
        logger.info("连接mongodb数据库成功")
        self.mongodb = self.client['wallpaper']
        self.uploader = uploader()


    def __del__(self):
        self.sql_client.close()


    def get_android_wallpaper(self):
        android_collection = self.mongodb[HANDLE_LIST["android"]["mongodb"]]
        wallpapers = android_collection.find({"is_handle": {"$exists": False}})
        for wallpaper in wallpapers:
            img_url = wallpaper['wp']
            # th_url = img_url+'&imageMogr2/thumbnail/!240x240r/gravity/Center/crop/240x240'
            img_id = get_uid(img_url)

            result1 = self.to_upload(img_id, img_url, HANDLE_LIST["android"]["mongodb"])
            # result2 = self.to_th_upload(img_id, th_url, HANDLE_LIST["android"]["mongodb"])

            # if result1 and result2:
            if result1:
                android_collection.update_one({'_id':wallpaper['_id']}, {'$set':{'is_handle':True, 'img_id': img_id}})


    def get_wallhaven_wallpaper(self):
        wallhaven_collection = self.mongodb[HANDLE_LIST["wallhaven"]["mongodb"]]
        wallpapers = wallhaven_collection.find({"is_handle":  False })
        for wallpaper in wallpapers:
            img_url = wallpaper['wp']
            # th_url = wallpaper['thumb']
            img_id = get_uid(img_url)

            result1 = self.to_upload(img_id, img_url, HANDLE_LIST["wallhaven"]["mongodb"])
            # result2 = self.to_th_upload(img_id, th_url, HANDLE_LIST["wallhaven"]["mongodb"])

            # if result1 and result2:
            if result1:
                wallhaven_collection.update_one({'_id':wallpaper['_id']}, {'$set':{'is_handle':True, 'img_id': img_id}})



    def to_upload(self, img_id, img_url, source):
        sql = "INSERT IGNORE INTO `wallpaper_wallpaper` (`img_id`, `url`, `thumbnail`, `source`, `add_time`) VALUES (%s, %s, %s, %s, %s);"
        url = 'https://yueeronline.xyz/{}.jpg'.format(img_id)
        thumbnail = url + '?imageView2/1/w/240/h/240/format/jpg/q/75|imageslim'
        data = (img_id, url, thumbnail, source, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        cursor = self.sql_client.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql, data)
            # 执行sql语句
            self.sql_client.commit()
            logger.info("壁纸已写入mysql数据库，id：{}, 链接：{}".format(img_id, url))
            logger.info("开始上传图片到七牛云...")
            result = self.uploader.upload(img_id, img_url)
            logger.info("上传结果: {}".format(result))
            if not result:
                raise Exception("上传图片到七牛云失败...")
            return True

        except Exception as e:
            # 发生错误时回滚
            logger.exception(e)
            logger.info("开始回滚...")
            self.sql_client.rollback()
            logger.info("回滚成功.")
        cursor.close()


    def main(self):
        # 上传安卓壁纸
        self.get_android_wallpaper() if HANDLE_LIST.get("android") else None
        # 上传wallhaven壁纸
        self.get_wallhaven_wallpaper() if HANDLE_LIST.get("wallhaven") else None
        logger.info('finish!')
        logger.info("今日壁纸上传七牛云并保存外链至mysql完毕！")


if __name__ == '__main__':
    try:
        AU = AutoUploader()
        AU.main()
        logger.info("wallpaper uploader success!")
    except Exception as e:
        logger.exception(e)


