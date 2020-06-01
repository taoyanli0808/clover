
import datetime

from clover.exts import db
from clover.models import CloverModel


class InterfaceModel(CloverModel):
    __tablename__ = 'interface'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    name = db.Column(db.String(64), index=True, comment="用例名称")
    type = db.Column(db.String(64), index=True, default="interface", comment="套件类型")
    sub_type = db.Column(db.String(64), index=True, default="interface", comment="[suite|interface]")
    method = db.Column(db.String(64), comment="请求方法")
    host = db.Column(db.String(512), comment="测试域名")
    path = db.Column(db.String(4096), comment="请求路径")
    header = db.Column(db.JSON, comment="http请求头")
    params = db.Column(db.JSON, comment="http请求参数")
    body = db.Column(db.JSON, comment="http请求体")
    verify = db.Column(db.JSON, comment="响应断言")
    extract = db.Column(db.JSON, comment="提取响应参数")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
