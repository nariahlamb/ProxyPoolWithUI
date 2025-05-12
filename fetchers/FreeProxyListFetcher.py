# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re

class FreeProxyListFetcher(BaseFetcher):
    """
    https://free-proxy-list.net
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """

        proxies = []
        # 使用正则表达式匹配 IP:Port 格式
        pattern = r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\:(?P<port>\d+)'

        
        # https代理 高级匿名代理ip提取
        html = requests.get('https://free-proxy-list.net', timeout=10).text
        matches = re.findall(pattern, html)

        # 构造结果列表
        result = [('http', match[0], int(match[1])) for match in matches]
        proxies.extend(result)
        # 构造结果列表
        result = [('https', match[0], int(match[1])) for match in matches]
        proxies.extend(result)

            
        return list(set(proxies))
