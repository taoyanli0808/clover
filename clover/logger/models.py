
import datetime

from clover.exts import db
from clover.models import CloverModel


class LoggerModel(CloverModel):
    __tablename__ = 'logger'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    type = db.Column(db.String(32), nullable=False, comment="用例类型[interface|automatiom]")
    sub_type = db.Column(db.String(32), nullable=False, comment="子类型[suite|case]")
    case = db.Column(db.Integer, nullable=False, comment="suite|interface的ID")
    logs = db.Column(db.JSON, nullable=False, comment="具体的日志内容")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
