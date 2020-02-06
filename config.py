
DEBUG = True
VERSION = '0.3.4'

MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True

CELERY_BROKER_URL='redis://127.0.0.1:6379/0'
# CELERY_RESULT_BACKEND=''
