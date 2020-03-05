
DEBUG = True
VERSION = '0.2.1'

MYSQL = {
    'user': 'root',
    'pswd': '456Juezui',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True