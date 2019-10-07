
from celery import Celery
from celery import platforms

from worker import config

app = Celery('tasks')
app.config_from_object(config)

platforms.C_FORCE_ROOT = True  # linux环境下，用于开启root也可以启动celery服务，默认是不允许root启动celery的


@app.task
def add(x, y):
    return x + y


if __name__ == '__main__':
    app.start()
