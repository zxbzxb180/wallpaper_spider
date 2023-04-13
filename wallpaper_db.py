from peewee import *
from settings import MYSQL_HOST,MYSQL_PORT,MYSQL_USER,MYSQL_PASSWORD

database = MySQLDatabase('web', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': MYSQL_HOST, 'port': MYSQL_PORT, 'user': MYSQL_USER, 'password': MYSQL_PASSWORD})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database


class WallpaperWallpaper(BaseModel):
    add_time = DateTimeField()
    img_id = CharField()
    source = CharField()
    thumbnail = CharField(null=True)
    url = CharField()
    is_delete = SmallIntegerField()

    class Meta:
        table_name = 'wallpaper_wallpaper'


