from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.report.service import ReportService
from clover.core.exception import catch_exception


class ReportView(CloverView):

    def __init__(self):
        super(ReportView, self).__init__()
        self.service = ReportService()

    @catch_exception
    def create(self):
        """
        :return:
        """
        pass

    @catch_exception
    def delete(self):
        """
        :return:
        """
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '删除测试报告时缺少必须的测试报告ID参数',
                'data': data,
            })

        try:
            self.service.delete(data)
            return jsonify({
                'status': 0,
                'message': '成功测试报告{0}'.format(data['id']),
                'data': {'id': data['id']},
                'total': 1
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '服务异常，请联系管理员！',
                'data': str(error)
            })

    @catch_exception
    def update(self):
        pass

    @catch_exception
    def search(self):
        """
        :return:
        """
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        try:
            count, results = self.service.search(data)
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

    @catch_exception
    def log(self):
        """
        :return:
        """
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '查询日志需要ID参数！',
                'data': data
            })

        try:
            result = self.service.log(data)
            if result is None:
                return jsonify({
                    'status': 0,
                    'message': "日志不存在！",
                    'data': []
                })
            else:
                return jsonify({
                    'status': 0,
                    'message': "日志不存在！",
                    'data': result
                })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '检索异常，请联系管理员！',
                'data': str(error)
            })
