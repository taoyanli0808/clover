
CELERY_TIMEZONE = 'Asia/Shanghai'
BROKER_BACKEND = 'mongodb'
BROKER_URL = 'mongodb://127.0.0.1:27017/transport'
CELERY_RESULT_BACKEND = 'mongodb://127.0.0.1:27017/backend'
CELERY_MONGODB_BACKEND_SETTINGS = {
    'host': '127.0.0.1',
    'port': 27017,
    'database': 'backend',
    'taskmeta_collection': 'result',
}
