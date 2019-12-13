FROM ubuntu

COPY . /data

WORKDIR /data/front

ADD ./front/package.json /data/front

# 安装依赖
RUN apt-get update && \
    apt-get -y install nodejs  && \
    apt-get -y install npm  && \
    npm install && \
    npm run generate && \
    apt-get -y install nginx  && \
    cp -f /data/nginx.conf /etc/nginx/nginx.conf && \
    apt-get -y install python3.7 && \
    pip3 --no-cache-dir install -r /data/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /data

CMD python3 clover.py runserver -h 0.0.0.0 && nginx