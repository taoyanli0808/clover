
import re
import os
import time
import json
import platform
import datetime

from config import VERSION


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


def convert_type(convertor, data):
    """
    :param convertor:
    :param data:
    :return:
    """
    try:
        if convertor == 'int':
            return int(data)
        elif convertor == 'float':
            return float(data)
        elif convertor == 'boolean':
            return bool(data)
        else:
            return str(data)
    except ValueError:
        return data
    except TypeError:
        return data


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


def get_python_dependency():
    dependency = {}
    require = os.path.join(os.getcwd(), 'requirements.txt')
    with open(require) as file:
        lines = file.readlines()
        for line in lines:
            if '>=' in line:
                name, version = line.split('>=')
            else:
                name, version = line.split('==')
            name, version = name.strip(), version.strip()
            dependency.setdefault(name, version)
    return dependency


def get_nodejs_dependency():
    require = os.path.join(os.getcwd(), 'package.json')
    with open(require) as file:
        data = json.load(file)
        dependency = {**data['dependencies'], **data['devDependencies']}
    return dependency


def allowed_file(filename):
    return  filename.rsplit('.', 1)[1].lower() in {'json','har'}


def friendly_datetime(data):
    """
    # 将字典里的datetime类型转化为字符串格式，方便前端展示。
    :param data:
    :return:
    """
    if not isinstance(data, (dict,)):
        return data

    for key, value in data.items():
        if not isinstance(value, (datetime.datetime,)):
            continue
        data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
    return data
