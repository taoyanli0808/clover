
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.report.service import Service


class ReportView(CloverView):

    def __init__(self):
        super(ReportView, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def search(self):
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

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
