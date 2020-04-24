
import datetime

from clover.exts import db
from clover.models import CloverModel


class DashboardModel(CloverModel):

    __tablename__ = 'dashboard'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    type = db.Column(db.String(64), index=True, comment="报告类型[interface|automation]")
    suite = db.Column(db.Integer, nullable=False, comment="任务维度[0为用例|1为套件]")
    name = db.Column(db.String(64), index=True, comment="用例或套件名称")
    identifier = db.Column(db.Integer, comment="用例或套件ID")
    statistics = db.Column(db.JSON(), comment="用例或套件的历史统计数据")
    score = db.Column(db.Integer, comment="用例或套件的得分")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")


if __name__ == '__main__':
    db.create_all()
