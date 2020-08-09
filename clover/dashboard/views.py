from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.dashboard.service import DashboardService
from clover.core.exception import catch_view_exception


class DashboardView(CloverView):

    def __init__(self):
        super(DashboardView, self).__init__()
        self.service = DashboardService()

    @catch_view_exception
    def info(self):
        data = self.service.get_info()
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })

    @catch_view_exception
    def suite(self):
        data = request.get_json()
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })
