# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re

class SSLProxiesFetcher(BaseFetcher):
    """
    https://www.sslproxies.org
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
        html = requests.get('https://www.sslproxies.org', timeout=10).text
        doc = pq(html)
        for line in doc('tr').items():
            tds = list(line('td').items())
            if len(tds) >= 2:
                ip = tds[0].text().strip().split(":")[0]
                port = tds[0].text().strip().split(":")[1]
                http = "http" if tds[0].text().strip().split(":")[6]=="no" else "https"
                if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                    proxies.append((http, ip, int(port)))
        
        return list(set(proxies))
