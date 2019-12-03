
from flask import Flask
from werkzeug.utils import import_string
from flask_sqlalchemy import SQLAlchemy

blueprints = [
    'clover.automation:automation',
    'clover.interface:interface',
    'clover.environment:environment',
]

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py', silent=True)

    db.init_app(app)

    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app
