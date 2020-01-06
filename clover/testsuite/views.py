
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.testsuite.service import Service


class TestSuiteView(CloverView):

    def __init__(self):
        super(TestSuiteView, self).__init__()

    def create(self):
        data = request.get_json()

        service = Service()
        result = service.create(data)
        if isinstance(result, tuple):
            code, msg = result
            return jsonify({
                'status': 500,
                'message': msg,
                'data': code
            })

        return jsonify({
            'status': 0,
            'message': '创建测试套件成功，套件ID[{}]'.format(id),
            'data': result
        })

        # try:
        #     service = Service()
        #     id = service.create(data)
        #     return jsonify({
        #         'status': 0,
        #         'message': '创建测试套件成功，套件ID[{}]'.format(id),
        #         'data': id
        #     })
        # except Exception as error:
        #     return jsonify({
        #         'status': 500,
        #         'message': '当创建套件时发生异常，请联系管理员！',
        #         'data': str(error)
        #     })

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
        data = request.values.to_dict()

        try:
            service = Service()
            count, results = service.search(data)
            return jsonify({
                'status': 0,
                'message': '成功检索到{}条数据'.format(count),
                'data': results,
                'total': count
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '检索异常，请联系管理员！',
                'data': str(error)
            })

    def trigger(self):
        """
        :param data:
        :return:
        """
        data = request.get_json()

        if 'cases' not in data or not data['cases']:
            return jsonify({
                'status': 400,
                'message': '请求缺少cases参数！',
                'data': data
            })

        try:
            service = Service()
            report_id = service.trigger(data)
            return jsonify({
                'status': 0,
                'message': '运行测试套件[{0}]成功，测试报告ID[{1}]'.format(id, report_id),
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '检索异常，请联系管理员！',
                'data': str(error)
            })
