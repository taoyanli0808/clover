import redis
from flask import Flask
from werkzeug.utils import import_string

import config
from clover.exts import db, client
from clover.urls import map_urls


blueprints = [
    'clover.suite:suite',
    'clover.interface:interface',
    'clover.environment:environment',
]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    app.app_context().push()
    map_urls(app)
    db.init_app(app)

    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    # create_stream()

    return app


def create_stream():
    """创建空stream"""
    if client.xlen('clover') == 0:
        try:
            stream_id = client.xadd('clover', {'businessData': ''})
            client.xgroup_create('clover', 'group_clover', id=0)
        except redis.exceptions.ResponseError as e:  # redis.exceptions.ResponseError
            pass  # print(e)
        finally:
            client.xack('clover', 'group_clover', stream_id)
            client.xdel('clover', stream_id)


app = create_app()
