
import time
import json
import platform
import datetime
import functools

from flask import request
from flask import jsonify
from flask import make_response

from clover.config import VERSION


def get_timestamp(data=None, format="%Y-%m-%d %H:%M:%S"):
    """
    :param data:
    :param format:
    :return:
    """
    if data is None:
        data = time.time()
    return time.strftime(format, time.localtime(data))


def get_mysql_error(error):
    """
    :param error:
    :return:
    """
    # (pymysql.err.ProgrammingError) (1146, "Table 'clover.suite' doesn't exist")
    error = error.args[0]
    error = error.strip("(pymysql.err.ProgrammingError) (").strip(")")
    return tuple(error.split(","))


def get_system_info():
    _platform = platform.platform()
    _platform = _platform.lower()
    if 'darwin' in _platform:
        _platform = 'darwin'
    elif 'windows' in _platform:
        _platform = 'windows'
    elif 'centos' in _platform:
        _platform = 'centos'
    elif 'ubuntu' in _platform:
        _platform = 'ubuntu'
    elif 'redhat' in _platform:
        _platform = 'redhat'
    else:
        _platform = 'linux'
    return {
        'platform': _platform,
        'python': platform.python_version(),
        'clover': VERSION,
    }


def allowed_file(filename):
    return  filename.rsplit('.', 1)[1].lower() in {'json','har'}


def friendly_datetime(data):
    """
    # 将字典里的datetime类型转化为字符串格式，方便前端展示。
    :param data:
    :return:
    """
    if isinstance(data, (datetime.datetime,)):
        return data.strftime("%Y-%m-%d %H:%M:%S")

    if not isinstance(data, (dict,)):
        return data

    for key, value in data.items():
        if not isinstance(value, (datetime.datetime,)):
            continue
        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return data


class CloverJSONEncoder(json.JSONEncoder):

    def default(self, data):
        if isinstance(data, datetime.datetime):
            return data.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, data)


def invalid_request_method(func):
    """
    # 捕获视图异常的装饰器
    :return:
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if request.method != 'POST':
            response = make_response(
                jsonify({
                    'status': 400,
                    'message': '请使用POST请求代替{}请求！'.format(request.method),
                    'data': {}
                }), 400
            )
            return response
        return func(*args, **kwargs)
    return wrapper
