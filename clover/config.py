# Clover全局配置
DEBUG = True
VERSION = '1.5.0'
DOMAIN = 'http://demo.52clover.cn'

# 全局功能配置
GLOBALS = {
    'timeout': {
        'connect': 3,
        'read': 60,
    },  # 全局接口超时配置，默认链接超时3秒，读超时60秒。
    'retry': 2,  # 全局接口重试配置，默认2次。
    'performance': 1000,  # 接口性能要求，1000ms以内。
}

# MySQL数据库配置
MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{pswd}@{host}:{port}/clover?charset=UTF8MB4&autocommit=true'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO = True

# 使用redis作为消息队列
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DATABASE = 0
REDIS_STREAM_NAME = 'clover'

# 功能控制，True则生效，False则无效
MODULE = {
    'join': True,  # 展示加入我们
    'task': False,  # 开发中的定时任务
    'keyword': False,  # 开发中的关键字配置
}

NOTIFY = {
    # 通知的触发事件，成功时通知还是失败时通知
    'event': ['success', 'skipped', 'failed', 'error'],
    # 通知的方式，企业微信还是email，或则配置的其它方式
    'channel': {
        'email': {
            'sender': 'zwx_towatt@126.com',
            'receiver': ['273518152@qq.com', 'zhouwenxi@towatt.com', '3317434061@qq.com'],
            'password': 'BFADJBLHHEXYWVMI',
            'smtp_host': 'smtp.126.com',

        },
        'wechat': 'b16f15f9-fda5-4894-9e3f-ae87542958c8',  # 这里是企微机器人的KEY配置
        'dingtalk': '4dd0b68415aabe0c6f36bb6a529a6fda6d128ae72ba8b69970f90398c69b36dd',  # 这里是钉钉机器人的access_token配置
    },
}
