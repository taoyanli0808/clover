FROM python:3.7.5-alpine

COPY . /clover

WORKDIR /clover/

# 安装依赖
RUN apk update && apk upgrade \
    && apk add build-base \
    && pip3 --no-cache-dir install -r /clover/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

CMD python clover.py runserver -h 0.0.0.0 && tail -f /dev/null