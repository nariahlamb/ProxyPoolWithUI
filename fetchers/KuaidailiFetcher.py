# encoding: utf-8

from .BaseFetcher import BaseFetcher
import requests
from pyquery import PyQuery as pq
import re
import json
from py_mini_racer import py_mini_racer

class KuaidailiFetcher(BaseFetcher):
    """
    https://www.kuaidaili.com/free
    """

    def fetch(self):
        """
        执行一次爬取，返回一个数组，每个元素是(protocol, ip, port)，portocal是协议名称，目前主要为http
        返回示例：[('http', '127.0.0.1', 8080), ('http', '127.0.0.1', 1234)]
        """
        
        urls = [f'https://www.kuaidaili.com/free/fps/{page}/' for page in range(1, 11)]

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'Cookie': '__tst_status=483636310#; EO_Bot_Ssid=2094989312; channelid=0;',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
        }

        # 创建 JavaScript 上下文
        ctx = py_mini_racer.MiniRacer()
        js_code = requests.get(urls[0], timeout=10, headers=headers).text

        # 使用正则表达式替换 document[...] 的赋值
        pattern = r'document\[(.*?)\]\s*=.*</script>'
        replacement = r'return "__tst_status="+a(0)+"#; "+ a(1)+"; channelid=0;"};calculate();'

        # 替换
        new_js_code = re.sub(pattern, replacement, js_code.replace("<script>","function calculate(){"), flags=re.DOTALL)
        headers["Cookie"]=ctx.eval(new_js_code)

        proxies = []

        for url in urls:
            html = requests.get(url, timeout=10, headers=headers).text
            match = re.search(r'const\s+fpsList\s*=\s*(.*?\]);', html, re.DOTALL)
            if match:
                fps_list_str = match.group(1)
                fps_list = json.loads(fps_list_str)
                result = [('http', item['ip'], item['port']) for item in fps_list]
                proxies.extend(result)
        
        proxies = list(set(proxies))

        return proxies
