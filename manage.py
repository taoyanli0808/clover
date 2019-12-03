
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

import pymysql
pymysql.install_as_MySQLdb()

from clover import db
from clover import create_app

app = create_app()

db.create_all()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
