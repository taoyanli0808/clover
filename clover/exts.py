
import config

from celery import Celery
from flask_sqlalchemy import SQLAlchemy

def create_celery():
    celery = Celery(
        'clover',
        broker=config.CELERY_BROKER_URL,
        # backend=app.config['CELERY_RESULT_BACKEND'],
    )
    celery.autodiscover_tasks(['clover.task'])
    return celery

db = SQLAlchemy()
task = create_celery()
