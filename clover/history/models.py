
import datetime

from clover.exts import db
from clover.models import CloverModel


class HistoryModel(CloverModel):
    __tablename__ = 'history'

    sid = db.Column(db.Integer, default=0, primary_key=True, comment="套件ID")
    cid = db.Column(db.Integer, default=0, primary_key=True, comment="接口ID")
    sname = db.Column(db.String(64), index=True, default="默认套件名称", comment="套件名称")
    cname = db.Column(db.String(64), index=True, default="默认用例名称", comment="用例名称")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(64), index=True, comment="项目")
    type = db.Column(db.String(64), default="interface", comment="套件类型")
    sub_type = db.Column(db.String(64), default="interface", comment="[suite|interface]")
    success = db.Column(db.Integer, default=0, comment="用例的成功运行次数")
    error = db.Column(db.Integer, default=0, comment="用例的出错运行次数")
    failed = db.Column(db.Integer, default=0, comment="用例的失败运行次数")
    skiped = db.Column(db.Integer, default=0, comment="用例的跳过运行次数")
    total = db.Column(db.Integer, default=0, comment="用例的全部运行次数")
    average = db.Column(db.Float, default=0.0, comment="用例的平均运行时间")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
