
import pymysql

from flask_cors import CORS
from flask_script import Server
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from clover import app
from clover.exts import db

pymysql.install_as_MySQLdb()


CORS(app, supports_credentials=True)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server())
manager.add_command("db", MigrateCommand)

if __name__ == '__main__':
    manager.run()
