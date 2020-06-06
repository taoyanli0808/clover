import gevent.monkey
gevent.monkey.patch_all()

import multiprocessing

debug = True
loglevel = 'debug'
bind = "0.0.0.0:5000"
pidfile = "logs/gunicorn.pid"
accesslog = "logs/flask_access.log"
errorlog = "logs/flask_error.log"
timeout = 300
daemon = True

# 启动的进程数
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
x_forwarded_for_header = 'X-FORWARDED-FOR'
