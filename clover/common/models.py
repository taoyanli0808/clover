
import datetime

from clover.exts import db
from clover.models import CloverModel


class LoggerModel(CloverModel):
    __tablename__ = 'logger'

    id = db.Column(db.Integer, nullable=False, primary_key=True, comment="ID")
    run_id = db.Column(db.Integer, nullable=False, comment="运行ID")
    case_id = db.Column(db.Integer, nullable=False, comment="用例ID")
    suite_id = db.Column(db.Integer, nullable=False, comment="套件ID")
    level = db.Column(db.Integer, nullable=False, comment="运行步骤")
    step = db.Column(db.String(64), nullable=False, comment="运行步骤")
    message = db.Column(db.String(1024), nullable=False, comment="运行消息")
    created = db.Column(db.DateTime, default=datetime.datetime.now, comment="创建时间")
