FROM node:10

LABEL maintainer="taoyanli0808@126.com"

COPY . /data

WORKDIR /data/front

RUN npm install && npm run generate

FROM python:3.7.5

WORKDIR /data

# 安装依赖
RUN apt-get update && apt-get -y install nginx && cp -f /data/nginx.conf /etc/nginx/nginx.conf
RUN pip3 --no-cache-dir install -r /data/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD python clover.py runserver -h 0.0.0.0 && nginx