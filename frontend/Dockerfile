# 前端 Dockerfile
FROM nginx:alpine

# 复制静态文件
COPY index.html /usr/share/nginx/html/
COPY admin.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

# 启动 Nginx
CMD ["nginx", "-g", "daemon off;"]

