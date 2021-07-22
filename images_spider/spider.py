import requests

def get_proxies():
    """
    获取公司代理
    :return: 公司代理
    """
    response = requests.get('http://47.111.74.232:5010/get/')
    proxy_dict = response.json()
    proxies = {
        'http': proxy_dict['proxy'],
        'https': proxy_dict['proxy']
    }
    return proxies


def retry_requests(url, **kwargs):
    """
    当请求出错时，重新执行此方法
    :param url: url
    :param kwargs: 任意requests.get()可选参数
    :return: 响应
    """
    for i in range(0, 10):
        print('请求中-----', url)
        try:
            #response = requests.get(url, proxies=get_proxies(), timeout=5, **kwargs)
            response = requests.get(url, timeout=5, **kwargs)
            print('请求成功----')
            return response

        except Exception as e:
            print(e)

    return False


def spider(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    }
    resp = retry_requests(url, headers=headers)
    if resp and resp.status_code == 200:
        datas = resp.json()['res']['vertical']
        for data in datas:
            id = data.get('id', '')
            img = data.get('img', '')
            image = retry_requests(img, headers=headers)
            if image.status_code == 200:
                with open('./images/{}.jpg'.format(id), 'wb') as f:
                    f.write(image.content)



def main():
    # 全部网页
    urls = ['http://service.picasso.adesk.com/v1/vertical/category/4e4d610cdf714d2966000003/vertical?&adult=false&order=new&skip={}'.format(i) for i in range(0, 450, 30)]
    for url in urls:
        spider(url)

if __name__ == "__main__":
    main()
