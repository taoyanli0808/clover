FROM python:3.7.5-alpine

COPY . /clover

WORKDIR /clover

# 安装nodejs，npm和nginx，redis服务，使用阿里云作为alpine源
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.10/main/" > /etc/apk/repositories \
    && apk update --no-cache \
    && apk upgrade --no-cache \
    && apk add build-base mariadb-dev \
    && apk add nodejs \
    && apk add npm \
    && apk add nginx \
    && apk add redis

# 编译前端资源
RUN npm install && npm run generate

# 安装python依赖
RUN pip3 --no-cache-dir install -r /clover/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 打开redis的后台模式
RUN echo "daemonize yes" >> /etc/redis.conf

# 开放MySQL和Redis（或RabbitMQ）的访问端口。
EXPOSE 3306
EXPOSE 6379

CMD gunicorn clover:app -c config.py \
    && nginx -c /clover/nginx.conf \
    && /usr/bin/redis-server /etc/redis.conf \
    && python worker.py > /clover/logs/worker.log
