import requests

def get_proxies():
    """
    获取代理
    :return: 代理
    """
    response = requests.get('http://139.198.181.33/get/')
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
            response = requests.get(url, timeout=5, **kwargs)
            print('请求成功----')
            return response

        except Exception as e:
            print(e)

    return False

