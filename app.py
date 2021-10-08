
import pymysql

from flask_cors import CORS
from flask_migrate import Migrate

from clover import app
from clover.exts import db

pymysql.install_as_MySQLdb()

CORS(app, supports_credentials=True)

migrate = Migrate(app, db)


if __name__ == '__main__':
    app.run()
