import time
import aiohttp
import asyncio
import pymongo
import traceback
from auto_upload import AutoUploader
from logger import logger
from settings import PROXY_IP, MONGO_HOST, MONGO_PORT, HANDLE_LIST, MONGO_USERNAME, MONGO_PASSWORD, MONGO_AUTH_SOURCE, MONGO_AUTH_MECHANISM
from lxml import etree



# 解析安卓壁纸
async def android_parser(response, session, obj):
    data_json = await response.json()
    collection = db[HANDLE_LIST['android']['mongodb']]
    datas = data_json.get('res', {}).get('vertical', [])
    for data in datas:
        data['crawl_date'] = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        data['crawl_time'] = time.time()
        collection.update_one({'id':data['id']}, {'$setOnInsert':data}, upsert=True)
        logger.info(data)


# 解析wallhaven壁纸
async def wallhaven_parser(response, session, obj):
    collection = db[HANDLE_LIST['wallhaven']['mongodb']]
    html = await response.text()
    tree = etree.HTML(html)
    wp_ids = tree.xpath("//li/figure/@data-wallpaper-id")
    figures = tree.xpath("//li/figure")
    for figure in figures:
        wp_id = figure.xpath("./@data-wallpaper-id")[0]
        wp_png = figure.xpath("./div/span[@class='png']")
        if wp_png:
            wp_format = 'png'
        else:
            wp_format = 'jpg'
        obj['id'] = wp_id
        obj['crawl_date'] = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        obj['crawl_time'] = time.time()
        obj['wp'] = 'https://w.wallhaven.cc/full/{}/wallhaven-{}.{}'.format(wp_id[0:2], wp_id, wp_format)
        obj['thumb'] = 'https://th.wallhaven.cc/small/{}/{}.jpg'.format(wp_id[0:2], wp_id)
        collection.update_one({'id':obj['id']}, {'$setOnInsert':obj}, upsert=True)
        logger.info(obj)


# 下载网页
async def download(obj):
    url = obj['url']
    headers=obj['headers']
    parser = parser_dict[obj['source']]
    print(url)
    async with asyncio.Semaphore(50):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            err = ""
            for i in range(20):
                try:
                    if obj.get("no_proxies"):
                        proxies = None
                    else:
                        proxies = await get_proxies()
                    async with session.get(url, proxy=proxies, headers=headers, timeout=16) as response:
                        if response.status == 200:
                            await parser(response, session, obj)
                            return
                except Exception as e:
                    print(traceback.format_exc())
                    err = e
            if err != "":
                logger.exception(err)

def gen_android_objs():
    if 'android' not in HANDLE_LIST.keys():
        return []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    return [{
                'url': 'http://service.picasso.adesk.com/v1/vertical/category/4e4d610cdf714d2966000003/vertical?&adult=false&order=new&skip={}'.format(i),
                'source': 'android',
                'headers': headers,
                'is_handle': False
            } for i in range(0, 450, 30)]

def gen_wallhaven_objs():
    if 'wallhaven' not in HANDLE_LIST.keys():
        return []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    return [{
                'url': 'https://wallhaven.cc/search?categories=110&purity=100&sorting=date_added&order=desc&ai_art_filter=0&page={}'.format(i),
                'source': 'wallhaven',
                'headers': headers,
                'is_handle': False,
                'no_proxies': True
            } for i in range(1, 11)]



async def get_proxies():
    """
    获取代理
    :return: 代理
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(PROXY_IP + '/get/', timeout=12) as response:
                proxy_dict = await response.json()
                return 'http://' + proxy_dict['proxy'] + '/'
        except Exception as e:
            logger.exception(e)


async def main():
    tasks = [download(obj) for obj in objs]
    results = await asyncio.gather(*tasks)



if __name__ == '__main__':
    try:
        parser_dict = {
         'android': android_parser,
         'wallhaven': wallhaven_parser
        }

        objs = []
        # 安卓壁纸
        objs.extend(gen_android_objs())
        # wallhaven壁纸
        objs.extend(gen_wallhaven_objs())


        if len(objs) == 0:
            logger.success("今日无壁纸任务!")
            exit()

        # 初始化mongodb
        client = pymongo.MongoClient(host=MONGO_HOST, port=MONGO_PORT, username=MONGO_USERNAME, password=MONGO_PASSWORD, authSource=MONGO_AUTH_SOURCE, authMechanism=MONGO_AUTH_MECHANISM)
        db = client['wallpaper']
        logger.info("初始化mongodb成功！")

        # 统计该爬虫的消耗时间
        logger.info('#' * 50)
        t1 = time.time()  # 开始时间

        # # 利用asyncio模块进行异步IO处理
        # loop = asyncio.get_event_loop()
        # tasks = [download(url) for url in urls]
        # # tasks = asyncio.gather(*tasks)
        # loop.run_until_complete(asyncio.wait(tasks))

        #另一种写法
        asyncio.run(main())

        t2 = time.time()  # 结束时间
        logger.info('使用aiohttp完成壁纸链接抓取，总共耗时：%s' % (t2 - t1))
        logger.info('#' * 50)

        # 立即开始下载图片，防止t参数失效
        AU = AutoUploader()
        AU.main()
        logger.success("每日壁纸程序执行完毕!")

    except Exception as e:
        logger.exception(e)



