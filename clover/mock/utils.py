
import time
import math
import hashlib

from functools import wraps

import pymysql

from flask import jsonify
from flask import request
from flask import session

from clover.config import SECRET_KEY


DATABASE = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'tyl.0808',
    'database': 'book',
    'port': 3306,
    'charset': 'utf8mb4'
}


def is_search(sql):
    """
    # 判断SQL语句是否为查询语句。
    :param sql:
    :return:
    """
    return 'select' in sql


def execute_sql(sql):
    """
    # 执行SQL代码，返回执行结果。
    # 如果是查询请求，返回所有查询结果
    # 如果是增、删、改请求则返回对应的ID
    :param sql:
    :return:
    """
    result = None
    db = pymysql.connect(**DATABASE)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    try:
        print(sql)
        cursor.execute(sql)
        db.commit()
        if is_search(sql):
            result = cursor.fetchall()
        else:
            result = cursor.lastrowid
    except pymysql.err.InternalError as error:
        db.rollback()
    finally:
        cursor.close()
        db.close()
    return result


def md5sum(source):
    """
    :param source:
    :return:
    """
    # 使用md5进行签名计算，如果指纹相同则认为验签通过。
    md5 = hashlib.md5()
    md5.update(source.encode('utf-8'))
    return md5.hexdigest()


def check_signature(func):
    """
    # 计算签名是否正确以及请求时间是否正常的装饰器
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.get_json()
        signature = data.pop('signature', None)

        # 提取请求参数里的签名，对请求进行相同方式排序。
        data.setdefault('secret', SECRET_KEY)
        keys = sorted(data.keys())
        source = ''.join([key + str(data[key]) for key in keys])

        # 如果请求时间超过当前时间60秒或晚于当前时间60秒，
        # 则认为请求异常，判定为抓取请求，验签不通过！
        time_difference = time.time() - data.pop('timestamp')
        if math.fabs(time_difference) > 60:
            return jsonify({
                'status': 400,
                'message': '时间异常，请同步系统时间！',
                'data': {}
            })

        if signature != md5sum(source):
            return jsonify({
                'status': 400,
                'message': '接口验签失败，请检查请求参数！',
                'data': {}
            })
        else:
            return func(*args, **kwargs)
    return wrapper


def login_required(func):
    """
    # 自定义登录装饰器，用于判断用户是否登录。
    # 用户登录后请求接口需要在header增加token。
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers['token']
        if token not in session:
            return jsonify({
                'status': 400,
                'message': '您尚未登录，请先登录！',
                'data': {}
            })
        else:
            return func(*args, **kwargs)
    return wrapper
