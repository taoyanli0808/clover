import redis
from flask_sqlalchemy import SQLAlchemy

from clover import config

db = SQLAlchemy()
engine = db.create_engine(
    config.SQLALCHEMY_DATABASE_URI,
    {
        'echo': False,  # 开启/关闭SQL语句打印，debug时使用True方便调试
        'pool_size': 100,
        'pool_recycle': 3600,
        'pool_pre_ping': True
    }
)

client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DATABASE,
    decode_responses=True,
)
