# encoding: utf-8

import os
import logging
import base64 # 导入 base64 库用于解码认证信息
from flask import Flask, Response # 导入 Response 用于返回自定义响应，特别是 401
from flask import jsonify, request, redirect, send_from_directory
from dotenv import load_dotenv

log = logging.getLogger('werkzeug')
log.disabled = True

try:
    from db import conn
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from db import conn

STATIC_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'frontend', 'deployment')

app = Flask(
    __name__,
    static_url_path='/web',
    static_folder=STATIC_FOLDER
)

############# 以下API可用于获取代理 ################

# 可用于测试API状态
@app.route('/ping', methods=['GET'])
def ping():
    return 'API OK'

# 随机获取一个可用代理，如果没有可用代理则返回空白
@app.route('/fetch_random', methods=['GET'])
def fetch_random():
    proxies = conn.getValidatedRandom(1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

############# 新增加接口int ################        

#api 获取协议为http的一条结果
@app.route('/fetch_http', methods=['GET'])
def fetch_http():
    proxies =conn.get_by_protocol('http', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_http_all', methods=['GET'])
def fetch_http_all():
    proxies = conn.get_by_protocol('http', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_https', methods=['GET'])
def fetch_https():
    proxies =conn.get_by_protocol('https', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_https_all', methods=['GET'])
def fetch_https_all():
    proxies = conn.get_by_protocol('https', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                
#api 获取协议为http的一条结果
@app.route('/fetch_socks4', methods=['GET'])
def fetch_socks4():
    proxies =conn.get_by_protocol('socks4', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为http的全部结果
@app.route('/fetch_socks4_all', methods=['GET'])
def fetch_socks4_all():
    proxies = conn.get_by_protocol('socks4', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
        
#api 获取协议为https的一条结果
@app.route('/fetch_socks5', methods=['GET'])
def fetch_socks5():
    proxies =conn.get_by_protocol('socks5', 1)
    if len(proxies) > 0:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    else:
        return ''

#api 获取协议为https的全部结果
@app.route('/fetch_socks5_all', methods=['GET'])
def fetch_socks5_all():
    proxies = conn.get_by_protocol('socks5', -1)
    if len(proxies) == 1:
        p = proxies[0]
        return f'{p.protocol}://{p.ip}:{p.port}'
    elif len(proxies) > 1:
        proxy_list = []
        for p in proxies:
            proxy_list.append(f'{p.protocol}://{p.ip}:{p.port}')
        return ','.join(proxy_list)
    else:
        return ''
                        
############# 新增加接口end ################    

# 获取所有可用代理，如果没有可用代理则返回空白
@app.route('/fetch_all', methods=['GET'])
def fetch_all():
    proxies = conn.getValidatedRandom(-1)
    proxies = [f'{p.protocol}://{p.ip}:{p.port}' for p in proxies]
    return ','.join(proxies)

############# 以下API主要给网页使用 ################

@app.route('/')
def index():
    return redirect('/web')

# 网页：首页
@app.route('/web', methods=['GET'])
@app.route('/web/', methods=['GET'])
def page_index():
    return send_from_directory(STATIC_FOLDER, 'index.html')

# 网页：爬取器状态
@app.route('/web/fetchers', methods=['GET'])
@app.route('/web/fetchers/', methods=['GET'])
def page_fetchers():
    return send_from_directory(STATIC_FOLDER, 'fetchers/index.html')

# 获取代理状态
@app.route('/proxies_status', methods=['GET'])
def proxies_status():
    proxies = conn.getValidatedRandom(-1)
    proxies = sorted(proxies, key=lambda p: f'{p.protocol}://{p.ip}:{p.port}', reverse=True)
    proxies = [p.to_dict() for p in proxies]

    status = conn.getProxiesStatus()

    return jsonify(dict(
        success=True,
        proxies=proxies,
        **status
    ))

# 获取爬取器状态
@app.route('/fetchers_status', methods=['GET'])
def fetchers_status():
    proxies = conn.getValidatedRandom(-1) # 获取所有可用代理
    fetchers = conn.getAllFetchers()
    fetchers = [f.to_dict() for f in fetchers]

    for f in fetchers:
        f['validated_cnt'] = len([_ for _ in proxies if _.fetcher_name == f['name']])
        f['in_db_cnt'] = conn.getProxyCount(f['name'])
    
    return jsonify(dict(
        success=True,
        fetchers=fetchers
    ))

# 清空爬取器状态
@app.route('/clear_fetchers_status', methods=['GET'])
def clear_fetchers_status():
    conn.pushClearFetchersStatus()
    return jsonify(dict(success=True))

# 设置是否启用特定爬取器,?name=str,enable=0/1
@app.route('/fetcher_enable', methods=['GET'])
def fetcher_enable():
    name = request.args.get('name')
    enable = request.args.get('enable')
    if enable == '1':
        conn.pushFetcherEnable(name, True)
    else:
        conn.pushFetcherEnable(name, False)
    return jsonify(dict(success=True))

############# 其他 ################

# 定义基础认证检查函数
@app.before_request
def check_basic_auth():
    """
    在每个请求前检查是否开启基础认证，如果开启则进行校验。
    """
    # 从 app.config 获取认证配置
    basic_auth_enabled = app.config.get('BASIC_AUTH', False)
    auth_user = app.config.get('BASIC_USER')
    auth_password = app.config.get('BASIC_PASSWORD')

    # 如果基础认证未开启，或者没有设置用户名/密码（即使开启了也没法验证），则直接放行
    if not basic_auth_enabled or not auth_user or not auth_password:
        return None # 返回 None 允许请求继续

    # 尝试获取 Authorization 头
    auth_header = request.headers.get('Authorization')

    # 检查 Authorization 头是否存在且格式正确 (Basic <base64编码串>)
    if not auth_header or not auth_header.startswith('Basic '):
        return Response(
            'Unauthorized: Basic Authentication Required',
            401, # Unauthorized 状态码
            {'WWW-Authenticate': 'Basic realm="Authentication Required"'} # 告诉客户端需要基础认证
        )

    # 提取 base64 编码的凭证
    encoded_credentials = auth_header.split(' ', 1)[1]

    try:
        # 解码 base64 字符串
        decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
        # 分割用户名和密码
        username, password = decoded_credentials.split(':', 1)

        # 校验用户名和密码
        if username == auth_user and password == auth_password:
            return None # 认证成功，允许请求继续
        else:
            # 用户名或密码不正确
            return Response(
                'Unauthorized: Invalid Credentials',
                401,
                {'WWW-Authenticate': 'Basic realm="Authentication Required"'}
            )

    except Exception as e:
        # 解码或分割出错 (例如 base64 格式错误)
        print(f"Basic Auth Error: {e}") # 可选：记录错误日志
        return Response(
            'Unauthorized: Invalid Authorization Header',
            401,
            {'WWW-Authenticate': 'Basic realm="Authentication Required"'}
        )

# 跨域支持，主要是在开发网页端的时候需要使用
def after_request(resp):
    ALLOWED_ORIGIN = ['0.0.0.0', '127.0.0.1', 'localhost']
    origin = request.headers.get('origin', None)
    if origin is not None:
        for item in ALLOWED_ORIGIN:
            if item in origin:
                resp.headers['Access-Control-Allow-Origin'] = origin
                resp.headers['Access-Control-Allow-Credentials'] = 'true'
    return resp
app.after_request(after_request)

def main(proc_lock):
    load_dotenv()  # 加载 .env 文件

    # 将 .env 中的相关配置加载到 app.config 中
    # 注意：从环境变量读取的值都是字符串，需要进行类型转换
    app.config['PORT'] = int(os.environ.get('PORT', '5000'))
    # 将字符串 'True'/'False' 转换为布尔值 True/False
    app.config['BASIC_AUTH'] = os.environ.get('BASIC_AUTH', 'False').lower() == 'true'
    app.config['BASIC_USER'] = os.environ.get('BASIC_USER')
    app.config['BASIC_PASSWORD'] = os.environ.get('BASIC_PASSWORD')

    
    if proc_lock is not None:
        conn.set_proc_lock(proc_lock)
    # 因为默认sqlite3中，同一个数据库连接不能在多线程环境下使用，所以这里需要禁用flask的多线程
    port = app.config['PORT'] # 从 app.config 获取端口
    print(f"Starting Flask server on http://0.0.0.0:{port}")
    if app.config['BASIC_AUTH']:
        print(f"Basic Authentication Enabled. User: {app.config['BASIC_USER']}")
    else:
         print("Basic Authentication Disabled.")

    app.run(host='0.0.0.0', port=port, threaded=False)

if __name__ == '__main__':
    main(None)
