
from clover import db
from clover.models import BaseModel


class Team(BaseModel):

    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(64), unique=True)
    project = db.Column(db.String(256), unique=True)

    def __repr__(self):
        return '<Team {id}>'.format(self.id)


class Variable(BaseModel):

    __tablename__ = 'variable'

    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(64), unique=True)
    project = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(64), unique=True)
    value = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Variable {id}>'.format(self.id)


class Snippet(BaseModel):

    __tablename__ = 'variable'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    mock = db.Column(db.String(64), unique=True)
    snippet = db.Column(db.String(1024), unique=True)

    def __repr__(self):
        return '<Snippet {id}>'.format(self.id)
