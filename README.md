# clover

A Simple and Easy-to-Use Automated Testing Platform (简单易用的测试平台)

## 试用

试用网址[Clover开源测试平台](http://demo.52clover.cn/)。

## 用户群

添加作者微信备注clover进入天使用户群
![用户微信群](https://cdn.jsdelivr.net/gh/wongqingbin/PicGo/clover/group.jpg)

## 如果您喜欢clover，可以请开发者喝杯82年的拉菲

![支持clover](https://cdn.jsdelivr.net/gh/wongqingbin/PicGo/clover/donation.jpg)

```bash
# 1.源码下载
git clone https://github.com/52clover/clover.git
# 2.下载mysql，并安装配置config
# 3.python需要的包，pip一键安装即可
pip install -r requirements.txt
# 4.进到项目下初始化数据库
flask db init
flask db migrate
flask db upgrade
# 4.项目运行run
python manage.py runserver
```
