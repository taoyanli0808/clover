
DEBUG = True

MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '192.168.0.101',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True