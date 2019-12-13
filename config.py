
DEBUG = True
# server config
SERVER = {
    'HOST': "0.0.0.0",
    'PORT': 9999,
    'DEBUG': True,
}

# database config
DATABASE = {
    'HOST': "127.0.0.1",
    'PORT': 27017,
    'USERNAME': "",
    'PASSWORD': "",
}

MYSQL_CONFIG = {
    'user': 'root',
    'pswd': 'tyl.0808',
    'host': '127.0.0.1',
    'port': 3306,
}
SQLALCHEMY_DATABASE_URI = "mysql://{user}:{pswd}@{host}:{port}/clover?charset=utf8".format(**MYSQL_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = True