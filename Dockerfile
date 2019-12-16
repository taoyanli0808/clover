FROM python:3.7.5-alpine

COPY . /clover

WORKDIR /clover/

# 安装nodejs，npm和nginx服务，使用阿里云作为alpine源
RUN echo "http://mirrors.aliyun.com/alpine/v3.10/main/" > /etc/apk/repositories \
    && apk add build-base \
    && apk add nodejs \
    && apk add npm \
    && apk add nginx

# 编译前端资源
RUN npm install && npm run generate

# 安装python依赖
RUN pip3 --no-cache-dir install -r /clover/requirements.txt -i https://mirrors.aliyun.com/pypi/simple

CMD gunicorn clover:app -c gconfig.py && nginx -c /clover/nginx.conf -g "daemon off;"