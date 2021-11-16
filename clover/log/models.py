
import datetime

from clover.exts import db
from clover.models import CloverModel


class LogModel(CloverModel):
    __tablename__ = 'log'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    report_id = db.Column(db.Integer, nullable=False, comment="关联的报告ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    interface_id = db.Column(db.Integer, nullable=False, comment="接口ID")
    interface_name = db.Column(db.String(64), index=True, comment="接口名称")
    start = db.Column(db.DateTime, default=datetime.datetime.now, comment="测试开始时间")
    end = db.Column(db.DateTime, default=datetime.datetime.now, comment="测试结束时间")
    duration = db.Column(db.Float, default=0.0, comment="测试持续时间")
    status = db.Column(db.Integer, default=0, comment="接口执行状态")
    init = db.Column(db.JSON, comment="初始化")
    request = db.Column(db.JSON, comment="处理请求")
    variable = db.Column(db.JSON, comment="替换变量")
    replace = db.Column(db.JSON, comment="替换变量")
    response = db.Column(db.JSON, comment="响应信息")
    validator = db.Column(db.JSON, comment="验证结果")
    performance = db.Column(db.JSON, comment="性能分析")
    extractor = db.Column(db.JSON, comment="传递数据")
    enable = db.Column(db.Integer, default=0, comment="记录是否有效|0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")
