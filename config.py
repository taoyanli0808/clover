
DEBUG = True
VERSION = '0.1.21'

<<<<<<< HEAD
SQLALCHEMY_DATABASE_URI='mysql://root:12345678@127.0.0.1:3306/clover?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS=True
=======
MYSQL = {
    'user': 'clover',
    'pswd': '52.clover',
    'host': '127.0.0.1',
    'port': '3306',
}
SQLALCHEMY_DATABASE_URI = 'mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8'.format(**MYSQL)
SQLALCHEMY_TRACK_MODIFICATIONS=True
>>>>>>> remote_origin/master
