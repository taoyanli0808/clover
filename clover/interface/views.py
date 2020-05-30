
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.interface.service import InterfaceService


class InterfaceView(CloverView):

    def __init__(self):
        super(InterfaceView, self).__init__()
        self.service = InterfaceService()

    def create(self):
        data = request.get_json()

        team = data.get('team', None)
        if not team:
            return jsonify({
                'status': 400,
                'message': '缺少团队参数！',
                'data': data,
            })

        project = data.get('project', None)
        if not project:
            return jsonify({
                'status': 400,
                'message': '缺少项目参数！',
                'data': data,
            })

        name = data.get('name', None)
        if not name:
            return jsonify({
                'status': 400,
                'message': '缺少测试用例名称！',
                'data': data,
            })

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
            id, status, message, result = self.service.create(data)
            return jsonify({
                'status': status,
                'message': message,
                'data': {
                    'id': id,
                    **result,
                },
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
            count = self.service.delete(data)
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
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '请选择您要更新的接口！',
                'data': data
            })

        try:
            id, status, message, result = self.service.update(data)
            return jsonify({
                'status': status,
                'message': message,
                'data': {
                    'id': id,
                    **result,
                },
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def search(self):

        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        try:
            count, result = self.service.search(data)
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

        result = self.service.trigger(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
        })
        # try:
        #     result = self.service.trigger(data)
        #     return jsonify({
        #         'status': 0,
        #         'message': 'ok',
        #         'data': result,
        #     })
        # except Exception as error:
        #     return jsonify({
        #         'status': 500,
        #         'message': str(error),
        #         'data': data
        #     })
