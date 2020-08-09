"""
# clover视图异常装饰器，当捕获视图异常时将返回状态码500和异常信息。
# author ：taoyanli0808
# date   ：2020年8月6日22:03:10
# version：1.0.0
"""

import traceback
from functools import wraps

from flask import jsonify
from flask import make_response

from sqlalchemy.exc import SQLAlchemyError

from clover.exts import db


class ResponseException(Exception): pass


def catch_exception(func):
    """
    # 捕获视图异常的装饰器
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError:
            print("捕获异常")
            db.session.rollback()
            response = make_response(
                jsonify({
                    'status': 500,
                    'message': '运行时数据库出错，请联系管理员！',
                    'data': {
                        'error': 'SQLAlchemyError',
                        'function': func.__name__,
                        'traceback': traceback.format_exc()
                    }
                }), 500
            )
            return response
        except Exception as error:
            response = make_response(
                jsonify({
                    'status': 500,
                    'message': '运行时代码出错，请联系管理员！',
                    'data': {
                        'error': str(error),
                        'function': func.__name__,
                        'traceback': traceback.format_exc()
                    }
                }), 500
            )
            return response
    return wrapper
