# 代理池部署指南

本文档提供了使用 Docker 和 Docker Compose 部署代理池服务的详细说明。

## 环境要求

- Docker
- Docker Compose

## 使用 Docker Compose 部署（推荐）

Docker Compose 是最简单的部署方式，只需几个命令即可完成部署。

### 1. 下载项目

```bash
git clone https://github.com/nariahlamb/ProxyPoolWithUI.git
cd ProxyPoolWithUI
```

### 2. 配置环境变量（可选）

项目默认配置已经可以正常工作，如果需要自定义配置，可以编辑 `.env` 文件：

```bash
# 复制样例配置文件
cp .env.sample .env
# 编辑配置文件
nano .env  # 或使用其他编辑器
```

配置项说明：

- `PORT`: 服务端口，默认为 5000
- `BASIC_AUTH`: 是否启用基本认证，`True` 或 `False`
- `BASIC_USER`: 基本认证用户名
- `BASIC_PASSWORD`: 基本认证密码

### 3. 构建并启动服务

```bash
docker-compose up -d
```

这个命令会在后台构建并启动代理池服务。

### 4. 查看服务状态

```bash
docker-compose ps
```

### 5. 查看服务日志

```bash
docker-compose logs -f
```

### 6. 停止服务

```bash
docker-compose down
```

## 使用 Docker 直接部署

如果您不想使用 Docker Compose，也可以直接使用 Docker 部署。

### 1. 构建镜像

```bash
docker build -t proxy_pool .
```

### 2. 运行容器

```bash
docker run -d \
  --name proxy_pool \
  -p 5000:5000 \
  -v $(pwd):/proxy \
  -e PORT=5000 \
  -e BASIC_AUTH=False \
  -e BASIC_USER=test \
  -e BASIC_PASSWORD=test \
  --restart always \
  proxy_pool
```

## 访问服务

部署完成后，可以通过以下方式访问服务：

- Web 管理界面：`http://<服务器IP>:5000`
- API 接口：
  - 获取随机代理：`http://<服务器IP>:5000/fetch_random`
  - 获取所有代理：`http://<服务器IP>:5000/fetch_all`
  - 获取HTTP代理：`http://<服务器IP>:5000/fetch_http`
  - 获取HTTPS代理：`http://<服务器IP>:5000/fetch_https`
  - 获取SOCKS5代理：`http://<服务器IP>:5000/fetch_socks5`
  - 更多API参见文档

## 数据持久化

代理池数据存储在 SQLite 数据库中，通过 Docker 数据卷挂载实现数据持久化。使用 Docker Compose 或上述 Docker 命令时，数据库文件会保存在宿主机项目目录下。

## 常见问题

### 1. 服务无法启动

检查端口是否被占用：

```bash
netstat -tunlp | grep 5000
```

如果端口被占用，可以在 `.env` 文件中修改 `PORT` 配置，或者停止占用端口的服务。

### 2. 无法获取代理

服务刚启动时，代理池是空的，需要等待爬虫爬取和验证代理，这个过程可能需要几分钟到几十分钟不等，请耐心等待。

### 3. 无法访问某些代理源

某些代理源可能在特定地区无法访问，这是正常的。系统会自动跳过不可用的代理源，使用其他可用的代理源爬取代理。

## 升级维护

### 更新到最新版本

```bash
# 停止服务
docker-compose down

# 拉取最新代码
git pull

# 重新构建并启动服务
docker-compose up -d --build
``` 