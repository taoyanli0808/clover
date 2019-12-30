
import datetime

from clover.exts import db
from clover.models import CloverModel


class TeamModel(CloverModel):

    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(64))
    project = db.Column(db.String(256))
    owner = db.Column(db.String(64))
    enable = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    # def __repr__(self):
    #     return '<Team {id}>'.format(self.id)


class VariableModel(CloverModel):

    __tablename__ = 'variable'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(64))
    project = db.Column(db.String(256))
    owner = db.Column(db.String(64))
    name = db.Column(db.String(64))
    value = db.Column(db.String(64))
    enable = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.datetime.now)
    updated = db.Column(db.DateTime, default=datetime.datetime.now)

    # def __repr__(self):
    #     return '<Variable {id}>'.format(self.id)


if __name__ == '__main__':
    pass