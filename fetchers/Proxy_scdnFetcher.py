# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re
import time
import json

class Proxy_scdnFetcher(BaseFetcher):
    """
    https://proxy.scdn.io/
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        proxies = []

        #只查询10*20条吧
        urls = ['https://proxy.scdn.io/api/get_proxy.php?protocol=http&count=20' for page in range(1, 11)]

        for url in urls:
            time.sleep(0.3)
            html = requests.get(url, timeout=10).text
            free = json.loads(html)['data']['proxies']
            result = [('http', item.split(":")[0], item.split(":")[1]) for item in free]
            proxies.extend(result)

        urls = ['https://proxy.scdn.io/api/get_proxy.php?protocol=https&count=20' for page in range(1, 11)]
        for url in urls:
            time.sleep(0.3)
            html = requests.get(url, timeout=10).text
            free = json.loads(html)['data']['proxies']
            result = [('https', item.split(":")[0], item.split(":")[1]) for item in free]
            proxies.extend(result)

        urls = ['https://proxy.scdn.io/api/get_proxy.php?protocol=socks4&count=20' for page in range(1, 11)]
        for url in urls:
            time.sleep(0.3)
            html = requests.get(url, timeout=10).text
            free = json.loads(html)['data']['proxies']
            result = [('socks4', item.split(":")[0], item.split(":")[1]) for item in free]
            proxies.extend(result)

        urls = ['https://proxy.scdn.io/api/get_proxy.php?protocol=socks5&count=20' for page in range(1, 11)]
        for url in urls:
            time.sleep(0.3)
            html = requests.get(url, timeout=10).text
            free = json.loads(html)['data']['proxies']
            result = [('socks5', item.split(":")[0], item.split(":")[1]) for item in free]
            proxies.extend(result)

        proxies = list(set(proxies))

        return proxies