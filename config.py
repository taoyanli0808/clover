
# Clover全局配置
DEBUG = True
VERSION = '0.5.1'

# MySQL数据库配置
MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True

# celery配置
CELERY_HOST = 'redis://127.0.0.1:6379/{}'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_BROKER_URL = CELERY_HOST.format(0)
CELERY_RESULT_BACKEND = CELERY_HOST.format(1)

# 功能控制，True则生效，False则无效
MODULE = {
    'join': True,   #展示加入我们
    'task': False,  #开发中的定时任务
}
