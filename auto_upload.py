import pymongo
import pymysql

import traceback
import hashlib
from datetime import datetime

from upload_2_qiniuyun import uploader

from logger import logger
from settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MONGO_HOST, MONGO_PORT


class AutoUploader():

    def __init__(self):
        self.sql_client = pymysql.connect(host=MYSQL_HOST,
                             port=MYSQL_PORT,
                             user=MYSQL_USER,
                             password=MYSQL_PASSWORD,
                             db=MYSQL_DB,
                             charset='utf8')
        logger.info("连接mysql数据库成功")
        self.client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
        logger.info("连接mongodb数据库成功")
        self.db = self.client['wallpaper']
        self.android_wallpaper = self.db['android_wallpaper']
        self.uploader = uploader()


    def __del__(self):
        self.sql_client.close()


    def get_android_wallpaper(self):
        wallpapers = self.android_wallpaper.find({"is_handle": {"$exists": False}})
        for wallpaper in wallpapers:
            print(wallpaper)
            #img_id = wallpaper['id']
            img_url = wallpaper['wp']

            m = hashlib.md5()
            m.update(img_url.encode(encoding='utf-8'))
            img_id = m.hexdigest()

            result1 = self.to_upload(img_id, img_url)
            result2 = self.to_th_upload(img_id, img_url)
            if result1 and result2:
                self.android_wallpaper.update_one({'_id':wallpaper['_id']}, {'$set':{'is_handle':True}})


    def to_upload(self, img_id, img_url):
        result = self.uploader.upload('adwp_{}'.format(img_id), img_url)
        if result:
            sql = "INSERT IGNORE INTO `wallpaper_wallpaper` (`img_id`, `url`, `source`, `add_time`) VALUES (%s, %s, %s, %s);"
            data = (img_id, 'https://yueeronline.xyz/adwp_{}.jpg'.format(img_id), 'android_wallpaper', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.save_to_mysql(sql, data)
            logger.info("壁纸已写入mysql数据库，id：{}, 链接：{}".format(img_id, img_url))
            return True

    def to_th_upload(self, img_id, img_url):
        th_url = img_url+'&imageMogr2/thumbnail/!240x240r/gravity/Center/crop/240x240'
        qiniu_url = 'https://yueeronline.xyz/adwp_th_{}.jpg'.format(img_id)
        result = self.uploader.upload('adwp_th_{}'.format(img_id), th_url)
        if result:
            sql = "UPDATE `wallpaper_wallpaper` SET `thumbnail` = '{}' WHERE img_id = '{}'".format(qiniu_url, img_id)
            self.save_to_mysql(sql)
            logger.info("壁纸已写入mysql数据库，id：{}, 链接：{}".format(img_id, img_url))
            return True

    def save_to_mysql(self, sql, data=None):
        cursor = self.sql_client.cursor()
        try:
            # 执行sql语句
            cursor.execute(sql, data)
            # 执行sql语句
            self.sql_client.commit()
        except Exception as e:
            # 发生错误时回滚
            print(traceback.format_exc())
            self.sql_client.rollback()
        cursor.close()


    def main(self):
        self.get_android_wallpaper()
        print('finish!')
        logger.info("今日壁纸上传七牛云并保存外链至mysql完毕！")


if __name__ == '__main__':
    try:
        AU = AutoUploader()
        AU.main()
        logger.info("wallpaper uploader success!")
    except Exception as e:
        logger.exception(e)


