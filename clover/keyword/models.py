
import datetime

from clover.exts import db
from clover.models import CloverModel


class KeywordModel(CloverModel):

    __tablename__ = 'keyword'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    name = db.Column(db.String(64), index=True, comment="关键字名称")
    description = db.Column(db.String(256), index=True, comment="关键字功能描述")
    keyword = db.Column(db.Text, comment="关键字代码")
    classify = db.Column(db.String(32), index=True, comment="关键字类型")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
