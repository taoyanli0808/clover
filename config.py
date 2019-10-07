
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

# kafka config
KAFKA = {
    'SERVER': ['localhost:9092'],
    'TOPIC': 'clover',
}
