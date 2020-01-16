
import re
import os
import time
import platform

from config import VERSION

from clover.common.HTMLTestRunner import HTMLTestRunner


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


def derivation(data, results):
    """
    :param data:
    :param results:
    :return:
    """
    # 这里如果data是空值或者变量没有设置则不处理。
    if not data or not results:
        return data

    variable = re.findall(r'\$\{(.+?)\}', data)
    if variable:
        variable = variable[0].strip()
        for result in results:
            if variable == result.name:
                return result.value
    else:
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
    return {
        'platform': platform.system(),
        'python': platform.python_version(),
        'clover': VERSION,
    }
