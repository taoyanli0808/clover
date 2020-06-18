from flask import jsonify
from flask import request

from clover.dashboard.service import DashboardService
from clover.views import CloverView


class DashboardView(CloverView):

    def __init__(self):
        super(DashboardView, self).__init__()
        self.service = DashboardService()

    def info(self):
        try:
            data = self.service.get_info()
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': None
            })

    def suite(self):
        data = request.get_json()
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': []
        })
