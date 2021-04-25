
import time

from flask import jsonify
from flask import request
from flask import session
from flask import make_response

from clover.views import CloverView
from clover.mock.service import MockService

from clover.mock.utils import md5sum
from clover.mock.utils import execute_sql as execute
from clover.mock.utils import login_required
from clover.mock.utils import check_signature


class MockView(CloverView):

    def __init__(self):
        super(MockView, self).__init__()
        self.service = MockService()

    def login(self):
        """
        # 模拟用户登录的接口，默认用户名clover，默认密码52.clover。
        # 如果用户名和密码不正确则报错，否则写入session与响应头。
        :return:
        """
        data = request.get_json()

        if 'username' not in data or not data['username']:
            return jsonify({
                'status': 400,
                'message': '登录请求缺少用户名！',
                'data': data
            })

        if 'password' not in data or not data['password']:
            return jsonify({
                'status': 400,
                'message': '登录请求缺少密码！',
                'data': data
            })

        # 判断用户名和密码是否正确。
        if data['username'] != 'clover' or data['password'] != '52.clover':
            return jsonify({
                'status': 400,
                'message': '错误的用户名或密码！',
                'data': data
            })

        # 通过用户名和密码计算md5签名，作为登录token值。
        data.setdefault('time', int(time.time()))
        source = "{username}{password}{time}".format(**data)
        __token = md5sum(source)

        # 将token存入session，值为用户名、密码和最后登录时间。
        session[__token] = data

        response = make_response(jsonify({
            'status': 0,
            'message': 'ok',
            'data': {}
        }))
        # 将token加入到响应头。
        response.headers["token"] = __token
        # 将token加入到cookie。
        response.set_cookie('token', __token)
        return response

    @login_required
    @check_signature
    def create(self):
        data = request.get_json()

        id = self.service.create(data)

        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })

    @login_required
    @check_signature
    def delete(self):
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '缺少需要删除的数据ID',
                'data': {}
            })

        result = self.service.delete(data)

        return jsonify({
            'status': 0,
            'message': '成功删除数据！',
            'data': result
        })

    @login_required
    @check_signature
    def update(self):
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '缺少需要更新的数据ID',
                'data': {}
            })

        result = self.service.update(data)

        return jsonify({
            'status': 0,
            'message': '成功更新数据！',
            'data': result
        })

    @login_required
    @check_signature
    def search(self):
        data = request.get_json()

        count, result = self.service.search(data)

        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'total': count,
        })
