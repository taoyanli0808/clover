
from flask import Flask
from werkzeug.utils import import_string

blueprints = [
    'clover.automation:automation',
    'clover.interface:interface',
    'clover.environment:environment',
]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app
