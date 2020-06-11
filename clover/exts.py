import redis
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()

client = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DATABASE,
    decode_responses=True,
)
