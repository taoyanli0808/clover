FROM python:3.7.5-alpine

COPY . /clover

WORKDIR /clover

# 安装nodejs，npm和nginx服务，使用阿里云作为alpine源
RUN echo "http://mirrors.ustc.edu.cn/alpine/v3.10/main/" > /etc/apk/repositories \
    && apk update --no-cache \
    && apk upgrade --no-cache \
    && apk add build-base mariadb-dev \
    && apk add nodejs \
    && apk add npm \
    && apk add nginx

# 编译前端资源
RUN npm install && npm run generate

# 安装python依赖
RUN pip3 --no-cache-dir install -r /clover/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 开放MySQL和Redis（或RabbitMQ）的访问端口。
EXPOSE 3306
EXPOSE 6379

CMD gunicorn clover:app -c gconfig.py \
    && nginx -c /clover/nginx.conf \
    && celery worker --app manage:task -c 4 > /clover/logs/task.log
