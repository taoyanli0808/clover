
import traceback

from flask import request
from flask import jsonify

from clover.environment.service import Service
from clover.environment.service import KeywordService
from clover.views import CloverView


class EnvironmentView(CloverView):

    def __init__(self):
        super(EnvironmentView, self).__init__()

    def create(self):

        data = request.get_json()
        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter team[{0}]".format(data['team']),
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter project[{0}]".format(data['project']),
                'data': data
            })

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter owner[{0}]".format(data['owner']),
                'data': data
            })

        try:
            service = Service()
            id = service.create(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def delete(self):

        data = request.get_json()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.detele(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):

        data = request.get_json()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.update(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):

        data = request.values.to_dict()

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter type[{0}]".format(data['type']),
                'data': data
            })

        try:
            service = Service()
            total, result = service.search(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def aggregate(self):

        data = request.get_json()

        try:
            service = Service()
            data = service.aggregate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })


class KeywordView(CloverView):

    def __init__(self):
        self.servce = KeywordService()

    def create(self):
        """
        :return:
        """
        data = request.get_json()

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '关键字需要定义名称!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少必要的测试数据!',
                'data': data
            })

        try:
            result = self.servce.create(data)
            return jsonify({
                'status': 0,
                'message': "创建关键字成功！",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def delete(self):
        """
        :return:
        """
        pass

    def update(self):
        """
        :return:
        """
        pass

    def search(self):
        """
        :return:
        """
        pass

    def debug(self):
        """
        :return:
        """
        data = request.get_json()

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '关键字需要定义名称!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少必要的测试数据!',
                'data': data
            })

        try:
            result = self.servce.debug(data)
            return jsonify({
                'status': 0,
                'message': "创建关键字成功！",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })
