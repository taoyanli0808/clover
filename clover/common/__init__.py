
import re
import os
import time
import json
import platform
import itertools

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


def derivation(data, keywords):
    """
    :param data:
    :param keywords:
    :return:
    """
    # 这里如果data是空值或者变量没有设置则不处理。
    if not data or not keywords:
        return data

    variables = re.findall(r'\$\{(.+?)\}', data)
    for variable in variables:
        if variable:
            variable = variable.strip()

            # 这里需要注意，变量的优先级是
            # 接口上下文变量 > 触发运行时指定变量 > 用户默认配置变量

            extract = keywords['extract']
            for result in extract:
                if variable == result['name']:
                    data = data.replace('${' + variable + '}', str(result['value']))

            trigger = keywords['trigger']
            for result in trigger:
                if variable == result['name']:
                    data = data.replace('${' + variable + '}', str(result['value']))

            default = keywords['default']
            for result in default:
                if variable == result['name']:
                    data = data.replace('${' + variable + '}', str(result['value']))

    return data


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


def rate_of_success(data):
    """
    :param data:
    :return:
    """
    rate = {
        'interface': 0,
        'assertion': 0,
        'percent': 0.0,
    }
    data = {** data, **rate}

    # 如果detail还没有数据，可能是用例没有执行完或异常，直接返回。
    if not data['detail']:
        return data

    # 统计接口，断言与成功率。
    details = data['detail'].values()
    results = [detail['result'] for detail in details if detail['result']]
    results = list(itertools.chain(*results))
    passed = len(list(filter(lambda x: x['status'] == 'passed', results)))
    percent = 100 * (passed / len(results)) if len(results) else 0
    percent = '{}%'.format(round(percent, 2))

    data['interface'] = len(details)
    data['assertion'] = len(results)
    data['percent'] = percent

    return data