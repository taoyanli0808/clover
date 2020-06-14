
from flask import jsonify
from flask import request

from clover.views import CloverView
# from clover.dashboard.service import DashboardService


class DashboardView(CloverView):

    def __init__(self):
        super(DashboardView, self).__init__()
        # self.service = DashboardService()

    def info(self):
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': {
                "summary": {
                    "team": 12,
                    "project": 65,
                    "suite": 57,
                    "interface": 283,
                    "keyword": 37,
                    "variable": 98,
                },
                "history": {
                    "2020-01": {
                        "interface": 192,
                        "suite": 43
                    },
                    "2020-02": {
                        "interface": 205,
                        "suite": 43
                    },
                    "2020-03": {
                        "interface": 211,
                        "suite": 44
                    },
                    "2020-04": {
                        "interface": 232,
                        "suite": 46
                    },
                    "2020-05": {
                        "interface": 265,
                        "suite": 52
                    },
                    "2020-06": {
                        "interface": 283,
                        "suite": 57
                    }
                },
                "latest":{
                    "suite": 5,
                    "interface": 18,
                    "variable": 11,
                    "keyword": 3
                }
            }
        })

    def suite(self):
        data = request.get_json()
        print(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': []
        })
