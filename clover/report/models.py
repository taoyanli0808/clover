
import datetime

from clover.exts import db
from clover.models import CloverModel


class ReportModel(CloverModel):
    __tablename__ = 'report'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    name = db.Column(db.String(64), index=True, comment="报告名称")
    type = db.Column(db.String(64), index=True, comment="报告类型[interface|automation]")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    suite_id = db.Column(db.Integer, nullable=False, comment="套件ID")
    suite_name = db.Column(db.String(64), index=False, comment="套件名")
    interface = db.Column(db.JSON, comment="测试接口个数")
    start = db.Column(db.DateTime, default=datetime.datetime.now, comment="测试开始时间")
    end = db.Column(db.DateTime, default=datetime.datetime.now, comment="测试结束时间")
    duration = db.Column(db.Float, default=0.0, comment="测试持续时间")
    platform = db.Column(db.JSON, comment="clover，python和平台信息")
    logid = db.Column(db.JSON, comment="执行接口的日志id列表")
    valid = db.Column(db.Integer, default=0, comment="日志是否有效|0有效，1调试")
    enable = db.Column(db.Integer, default=0, comment="记录是否有效|0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
