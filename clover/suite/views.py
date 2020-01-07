
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.suite.service import Service


class SuiteView(CloverView):

    def __init__(self):
        super(SuiteView, self).__init__()

    def create(self):
        data = request.get_json()

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': '请选择团队！',
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': '请选择项目！',
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': '请选择项目！',
                'data': data
            })

        if 'type' not in data or not data['type']:
            return jsonify({
                'status': 400,
                'message': '请求缺少类型参数，类型必须为[interface|automation]！',
                'data': data
            })

        if 'cases' not in data or not data['cases']:
            return jsonify({
                'status': 400,
                'message': '请选择要创建套件的用例！',
                'data': data
            })

        try:
            service = Service()
            id = service.create(data)
            return jsonify({
                'status': 0,
                'message': '创建测试套件成功，套件ID[{}]'.format(id),
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '当创建套件时发生异常，请联系管理员！',
                'data': str(error)
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

        service = Service()
        result = service.trigger(data)
        return jsonify({
            'status': 0,
            'message': '运行测试套件[{0}]成功，测试报告ID[{1}]'.format(id, 111),
            'data': result
        })

        # try:
        #     service = Service()
        #     result = service.trigger(data)
        #     return jsonify({
        #         'status': 0,
        #         'message': '运行测试套件[{0}]成功，测试报告ID[{1}]'.format(id, report_id),
        #         'data': result
        #     })
        # except Exception as error:
        #     return jsonify({
        #         'status': 500,
        #         'message': '运行套件出错，请联系管理员！',
        #         'data': str(error)
        #     })
