
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.interface.service import Service
from clover.common.executor import Executor


class InterfaceView(CloverView):

    def __init__(self):
        super(InterfaceView, self).__init__()

    def create(self):
        data = request.get_json()

        method = data.get('method', None)
        if not method:
            return jsonify({
                'status': 400,
                'message': '缺少请求方法参数！',
                'data': data,
            })

        host = data.get('host', None)
        if not host:
            return jsonify({
                'status': 400,
                'message': '缺少请求域名！',
                'data': data,
            })

        path = data.get('path', None)
        if not path:
            return jsonify({
                'status': 400,
                'message': '缺少请求路径！',
                'data': data,
            })

        try:
            service = Service()
            id = service.create(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def delete(self):

        data = request.get_json()

        if 'id_list' not in data or not data['id_list']:
            return jsonify({
                'status': 400,
                'message': '请选择您要删除的接口！',
                'data': data
            })
        try:
            service = Service()
            count = service.delete(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': count,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '服务器出错，请联系管理员！',
                'data': data
            })

    def update(self):
        pass

    def search(self):

        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        try:
            service = Service()
            count, result = service.search(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': count,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def debug(self):
        data = request.get_json()

        name = data.get('name', None)
        if not name:
            return jsonify({
                'status': 400,
                'message': '接口测试用例需要用例名称！',
                'data': data,
            })

        method = data.get('method', None)
        if not method:
            return jsonify({
                'status': 400,
                'message': '接口测试用例需要正确的请求方法，可选值为[GET|POST|PUT|DELETE]！',
                'data': data,
            })

        host = data.get('host', None)
        if not host:
            return jsonify({
                'status': 400,
                'message': '接口测试用例需要指定域名，例如[https://github.com]！',
                'data': data,
            })

        path = data.get('path', None)
        if not path:
            return jsonify({
                'status': 400,
                'message': '接口测试用例需要指定路径，例如[/taoyanli0808/clover]！',
                'data': data,
            })

        try:
            executor = Executor()
            data = executor.execute(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '运行时错误，请联系管理员！',
                'data': {}
            })

    def trigger(self):
        # 这里支持GET与POST请求，获取参数方法不同。
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        id = data.get('id', None)
        if not id:
            return jsonify({
                'status': 400,
                'message': '运行接口用例需要指定ID参数',
                'data': data,
            })

        try:
            service = Service()
            result = service.trigger(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })
