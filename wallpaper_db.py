from peewee import *

database = MySQLDatabase('web', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '172.17.0.1', 'port': 3306, 'user': 'web', 'password': 'cx6222580'})

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

    class Meta:
        table_name = 'wallpaper_wallpaper'


