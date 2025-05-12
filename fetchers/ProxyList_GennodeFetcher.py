# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re
import time

class ProxyList_GennodeFetcher(BaseFetcher):
    """
    https://geonode.com/free-proxy-list
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        #只查询4*500条吧
        urls = [f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={page}' for page in range(1, 5)]

        proxies = []

        for url in urls:
            time.sleep(1)
            html = requests.get(url, timeout=10).text
            free = json.loads(data)['data']
            result = [(item['protocols'][0], item['ip'], item['port']) for item in free]
            proxies.extend(result)

        proxies = list(set(proxies))

        return proxies
