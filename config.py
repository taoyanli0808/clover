
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

# MySQL config
DB_CONFIG = {
    'HOST': "127.0.0.1",
    'PORT': 3306,
    'DBNAME': 'clover',
    'USERNAME': "root",
    'PASSWORD': "admin123456",
    'CHARSET': 'utf8',
}

# kafka config
KAFKA = {
    'SERVER': ['localhost:9092'],
    'TOPIC': 'clover',
}
