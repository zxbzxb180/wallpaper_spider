#coding:utf-8
import time
import datetime
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import requests
import pymongo
from peewee import fn

from wallpaper_db import database, WallpaperWallpaper
from settings import WORDPRESS_URL,WORDPRESS_USER,WORDPRESS_PASSWORD,WORDPRESS_POST_NUM
from logger import logger

class WPPost():
    def __init__(self):
        self.wp = Client(WORDPRESS_URL, WORDPRESS_USER, WORDPRESS_PASSWORD)
        self.post = WordPressPost()
        self.post.title = '{} 壁纸分享'.format(time.strftime("%Y-%m-%d",time.localtime(time.time())))
        self.post.post_status = 'publish'  #文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
        self.post.terms_names = {
                              'post_tag': ['壁纸'], #文章所属标签，没有则自动创建
                              'category': ['壁纸分享'] #文章所属分类，没有则自动创建
                             }
        self.content = '本站收集的所有壁纸,仅为壁纸爱好者分享,禁止商用或进行其他不当行为！如侵犯到权益,请联系我立刻删除。\r\n \r\n'
        self.post.comment_status = 'open'
        self.sql_client = database
        self.sql_client.connect()
        self.wallpaper = WallpaperWallpaper


    def get_wallpaper(self):
        event_date_dt = datetime.datetime.strptime(time.strftime("%Y-%m-%d",time.localtime(time.time())), '%Y-%m-%d')
        wallpapers = list(self.wallpaper.select().where((self.wallpaper.add_time > event_date_dt) & (self.wallpaper.add_time < event_date_dt + datetime.timedelta(days=1)) & (self.wallpaper.is_delete == 0)).limit(WORDPRESS_POST_NUM))
        i = 0
        if not wallpapers:
            self.content += '很抱歉^_^，今日没有壁纸哦~'
            return
        for wallpaper in wallpapers:
            i += 1
            wp = wallpaper.url
            wp_th = wallpaper.thumbnail
            self.content += '!{{image {}}}({})[{}?resize=240,240] '.format(i, wp, wp_th)
    def __del__(self):
        self.sql_client.close()

    def post_wallpaper(self):
        self.post.content = self.content
        self.post.id = self.wp.call(posts.NewPost(self.post))
        print('post success! {}'.format(id))


    def main(self):
        self.get_wallpaper()
        if self.content:
            self.post_wallpaper()

if __name__ == '__main__':
    try:
        wpp = WPPost()
        wpp.main()
        logger.success("WordPress每日壁纸文章发布成功!")
    except Exception as e:
        logger.exception(e)
