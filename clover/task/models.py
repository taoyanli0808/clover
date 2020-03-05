
import datetime

from clover.exts import db
from clover.models import CloverModel


class TaskModel(CloverModel):
    __tablename__ = 'task'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    name = db.Column(db.String(64), index=True, comment="任务名称")
    cron = db.Column(db.String(64), index=True, comment="表达式")
    variable = db.Column(db.JSON, comment="触发变量")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
