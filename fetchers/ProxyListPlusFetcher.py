# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re
import time

class ProxyListPlusFetcher(BaseFetcher):
    """
    https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        urls = [f'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{page}' for page in range(1, 7)]

        for url in urls:
            time.sleep(1)
            html = requests.get(url, timeout=10).text
            doc = pq(html)
            for line in doc('tr').items():
                tds = list(line('td').items())
                if len(tds) >= 2:
                    ip = tds[0].text().strip().split(":")[1]
                    port = tds[0].text().strip().split(":")[2]
                    if re.match(ip_regex, ip) is not None and re.match(port_regex, port) is not None:
                        proxies.append(('http', ip, int(port)))


        proxies = list(set(proxies))

        return proxies
