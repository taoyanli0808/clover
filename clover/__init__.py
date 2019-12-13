
from flask import Flask
from werkzeug.utils import import_string

import config

blueprints = [
    'clover.automation:automation',
    'clover.interface:interface',
    'clover.environment:environment',
]


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    app.app_context().push()

    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app
