
import datetime

from clover.exts import db
from clover.models import CloverModel


class TeamModel(CloverModel):

    __tablename__ = 'team'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    owner = db.Column(db.String(64), index=True, comment="负责人")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")

    # def __repr__(self):
    #     return '<Team {id}>'.format(self.id)


class VariableModel(CloverModel):

    __tablename__ = 'variable'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    owner = db.Column(db.String(64), index=True, comment="负责人")
    name = db.Column(db.String(64), index=True, comment="变量名")
    value = db.Column(db.String(64), index=True, comment="变量值")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")

    # def __repr__(self):
    #     return '<Variable {id}>'.format(self.id)


if __name__ == '__main__':
    pass