# Clover全局配置
DEBUG = True
VERSION = '1.0.0'

# MySQL数据库配置
MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True

# 使用redis作为消息队列
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DATABASE = 0

# 功能控制，True则生效，False则无效
MODULE = {
    'join': True,   # 展示加入我们
    'task': False,  # 开发中的定时任务
    'keyword': False, # 开发中的关键字配置
}

# 企业微信配置
WECHAT = {
    'key': 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', # 这里是企业微信机器人的key
    'template': {
        'msgtype': 'markdown',
        'markdown': {
            'content': 'Clover平台运行报告！\n'+
            '>类型:<font color=\"comment\">{type}</font>\n' +
            '>团队:<font color=\"comment\">{team}</font>\n' +
            '>项目:<font color=\"comment\">{project}</font>\n' +
            '>名称:<font color=\"comment\">{name}</font>\n' +
            '>接口:<font color=\"comment\">{interface}个</font>\n' +
            '>断言:<font color=\"comment\">{verify}个</font>\n' +
            '>成功率:<font color=\"comment\">{percent}</font>\n' +
            '>开始时间:<font color=\"comment\">{start}</font>\n' +
            '>结束时间:<font color=\"comment\">{end}</font>\n' +
            '[测试报告-{id}](http://www.52clover.cn/report/detail?id={id})'
        }
    }
}

# 邮箱配置
EMAIL = {
    'sender': '12345678@qq.com',
    'receiver': ['12345678@qq.com'],
    'password': '',
    'smtp_host': 'smtp.qq.com',
}

NOTIFY = {
    # 通知的触发事件，成功时通知还是失败时通知
    'event': ['success', 'failed'],
    # 通知的方式，企业微信还是email，或则配置的其它方式
    'channel': ['email'],
}