
import datetime

from clover.exts import db
from clover.models import CloverModel


class SuiteModel(CloverModel):
    __tablename__ = 'suite'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    name = db.Column(db.String(64), index=True, comment="套件名称")
    type = db.Column(db.String(64), index=True, comment="套件类型")
    cases = db.Column(db.JSON, comment="测试用例列表")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
