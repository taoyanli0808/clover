"""
# 用于记录任务执行的信息。
"""

import enum
import datetime

from clover import db
from clover.logger.models import LoggerModel


class LogLevel(enum.Enum):
    """
    # debug为调试信息
    # info为日志默认输出等级
    # warn为requests请求异常信息
    # error为clover异常信息
    """
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4


class Logger(object):

    logs = []

    @classmethod
    def log(cls, message, step, tag=[], level=LogLevel.INFO):
        cls.logs.append({
            'time': datetime.datetime.now(),
            'level': level,
            'step': step,
            'message': message,
            'tag': tag
        })

    @classmethod
    def clear(cls):
        cls.logs = []

    @classmethod
    def to_dict(cls):
        def translate(data):
            data['time'] = data['time'].strftime("%Y-%m-%d %H:%M:%S")
            data['level'] = data['level'].name.lower()
            return data
        return [translate(log) for log in cls.logs]

    @classmethod
    def save(cls, _type, sub_type, case):
        data = {
            'type': _type,
            'sub_type': sub_type,
            'case': case,
            'logs': cls.to_dict(),
        }
        # print(type(logs), logs)
        # print(type(logs['logs']), logs['logs'])
        # print(type(logs['logs'][0]), logs['logs'][0])
        print(50 * '*')
        print(type(data['logs'][0]['level']), data['logs'][0]['level'])
        print(50 * '*')
        for log in data['logs']:
            print(type(log['level']), log['level'])
        print(50 * '*')
        model = LoggerModel(**data)
        db.session.add(model)
        db.session.commit()