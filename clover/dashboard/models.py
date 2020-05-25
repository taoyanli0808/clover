
import datetime

from clover.exts import db
from clover.models import CloverModel


class InterfaceDashboardModel(CloverModel):

    __tablename__ = 'interface_dashboard'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    name = db.Column(db.String(64), index=True, comment="接口名称")
    identifier = db.Column(db.Integer, index=True, comment="接口ID")
    status = db.Column(db.Integer, index=True, comment="接口运行状态[0-passed|1-failed|2-error|3-skiped]")
    remark = db.Column(db.String(256), index=True, comment="备注原因")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")


class InterfaceSuiteDashboardModel(CloverModel):

    __tablename__ = 'interface_suite_dashboard'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    team = db.Column(db.String(64), index=True, comment="团队")
    project = db.Column(db.String(256), index=True, comment="项目")
    name = db.Column(db.String(64), index=True, comment="套件名称")
    identifier = db.Column(db.Integer, comment="套件ID")
    status = db.Column(db.Integer, comment="套件运行状态[0-passed|1-failed|2-error|3-skiped]")
    remark = db.Column(db.String(256), index=True, comment="备注原因")
    enable = db.Column(db.Integer, default=0, comment="0有效，1无效")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
    updated = db.Column(db.DateTime, default=datetime.datetime.now, comment="修改时间")


if __name__ == '__main__':
    db.create_all()
