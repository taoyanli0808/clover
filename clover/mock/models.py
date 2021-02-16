
import datetime

from clover.exts import db
from clover.models import CloverModel


class MockModel(CloverModel):
    __tablename__ = 'mock'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    name = db.Column(db.String(64), index=True, comment="图书名")
    author = db.Column(db.String(64), index=True, comment="图书作者")
    price = db.Column(db.Float(), default=0.0, comment="图书价格")
    publisher = db.Column(db.String(64), index=True, comment="出版社")
    type = db.Column(db.Integer, default=1, comment="类型：1科技 2历史 3教育 4社科 5文艺")
    isbn = db.Column(db.String(13), default="1", comment="国际标准书号")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    publish = db.Column(db.DateTime, default=datetime.datetime.now, comment="出版时间")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
