#!/bin/bash

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 显示帮助信息
show_help() {
    echo -e "${GREEN}ProxyPool 管理脚本${NC}"
    echo "用法: ./manage.sh [命令]"
    echo ""
    echo "命令:"
    echo "  start       启动服务"
    echo "  stop        停止服务"
    echo "  restart     重启服务"
    echo "  status      查看服务状态"
    echo "  logs        查看服务日志"
    echo "  update      更新到最新版本"
    echo "  create-env  创建环境变量文件"
    echo "  help        显示帮助信息"
    echo ""
}

# 检查 Docker 是否安装
check_docker() {
    if ! [ -x "$(command -v docker)" ]; then
        echo -e "${RED}错误: Docker 未安装${NC}" >&2
        echo "请先安装 Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! [ -x "$(command -v docker-compose)" ]; then
        echo -e "${RED}错误: Docker Compose 未安装${NC}" >&2
        echo "请先安装 Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
}

# 启动服务
start_service() {
    echo -e "${YELLOW}正在启动 ProxyPool 服务...${NC}"
    docker-compose up -d
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}服务启动成功!${NC}"
        echo -e "请访问: ${GREEN}http://localhost:5000${NC}"
    else
        echo -e "${RED}服务启动失败，请检查日志${NC}"
    fi
}

# 停止服务
stop_service() {
    echo -e "${YELLOW}正在停止 ProxyPool 服务...${NC}"
    docker-compose down
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}服务已停止${NC}"
    else
        echo -e "${RED}服务停止失败，请检查日志${NC}"
    fi
}

# 重启服务
restart_service() {
    echo -e "${YELLOW}正在重启 ProxyPool 服务...${NC}"
    docker-compose restart
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}服务重启成功!${NC}"
        echo -e "请访问: ${GREEN}http://localhost:5000${NC}"
    else
        echo -e "${RED}服务重启失败，请检查日志${NC}"
    fi
}

# 查看服务状态
check_status() {
    echo -e "${YELLOW}ProxyPool 服务状态:${NC}"
    docker-compose ps
}

# 查看服务日志
view_logs() {
    echo -e "${YELLOW}ProxyPool 服务日志:${NC}"
    docker-compose logs -f
}

# 更新到最新版本
update_service() {
    echo -e "${YELLOW}正在更新 ProxyPool 服务...${NC}"
    git pull
    docker-compose down
    docker-compose build
    docker-compose up -d
    echo -e "${GREEN}服务更新成功!${NC}"
}

# 创建环境变量文件
create_env_file() {
    if [ -f .env ]; then
        echo -e "${YELLOW}环境变量文件 .env 已存在，是否覆盖? [y/N]${NC}"
        read answer
        if [[ $answer != "y" && $answer != "Y" ]]; then
            echo -e "${YELLOW}操作已取消${NC}"
            return
        fi
    fi
    
    echo -e "${YELLOW}正在创建环境变量文件...${NC}"
    cat > .env << EOF
PORT=5000
BASIC_AUTH=False
BASIC_USER=test
BASIC_PASSWORD=test
EOF
    echo -e "${GREEN}环境变量文件创建成功!${NC}"
}

# 主逻辑
check_docker

if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case $1 in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    update)
        update_service
        ;;
    create-env)
        create_env_file
        ;;
    help|*)
        show_help
        ;;
esac 