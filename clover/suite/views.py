
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.suite.service import SuiteService
from clover.core.exception import catch_exception


class SuiteView(CloverView):

    def __init__(self):
        super(SuiteView, self).__init__()
        self.service = SuiteService()

    @catch_exception
    def api_v1_suite_create(self):
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

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '请填写套件名称！',
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

        id = self.service.create(data)
        return jsonify({
            'status': 0,
            'message': '创建测试套件成功，套件ID[{}]'.format(id),
            'data': id
        })

    @catch_exception
    def api_v1_suite_delete(self):
        data = request.get_json()

        if 'id_list' not in data or not data['id_list']:
            return jsonify({
                'status': 400,
                'message': '请选择您要删除的接口！',
                'data': data
            })

        count = self.service.delete(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': count,
        })

    @catch_exception
    def api_v1_suite_update(self):
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '请填写套件ID！',
                'data': data
            })

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '请填写套件名称！',
                'data': data
            })

        if 'cases' not in data or not data['cases']:
            return jsonify({
                'status': 400,
                'message': '请选择要更新套件的用例！',
                'data': data
            })

        result = self.service.update(data)
        return jsonify({
            'status': 0,
            'message': 'success',
            'data': result,
        })

    @catch_exception
    def api_v1_suite_search(self):
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        count, results = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': '成功检索到{}条数据'.format(count),
            'data': results,
            'total': count
        })

    @catch_exception
    def api_v1_suite_trigger(self):
        """
        :param data:
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '运行接口用例需要指定ID参数',
                'data': data
            })

        result = self.service.trigger(data)
        return jsonify({
            'status': 0,
            'message': '运行测试套件[{0}]成功，测试报告ID[{1}]'.format(id, result),
            'data': result
        })

    @catch_exception
    def api_v1_suite_switch(self):
        data = request.get_json()
        if 'id_list' not in data or not data['id_list']:
            return jsonify({
                'status': 400,
                'message': '请选择您要更改开关状态的接口！',
                'data': data
            })

        if 'status' not in data:
            return jsonify({
                'status': 400,
                'message': '请选择您要更改接口的状态！',
                'data': data
            })

        result = self.service.switch(data)
        return jsonify({
            'status': 0,
            'message': '套件已开启' if data['status'] else '套件已禁用',
            'data': result,
        })
