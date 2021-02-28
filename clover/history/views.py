from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.core.exception import catch_exception
from clover.history.service import HistoryService


class HistoryView(CloverView):

    def __init__(self):
        super(HistoryView, self).__init__()
        self.service = HistoryService()

    @catch_exception
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

        sid = data.get('sid', None)
        if not sid:
            return jsonify({
                'status': 400,
                'message': '缺少套件ID！',
                'data': data,
            })

        cid = data.get('cid', None)
        if not cid:
            return jsonify({
                'status': 400,
                'message': '缺少用例ID！',
                'data': data,
            })

        sname = data.get('sname', None)
        if not sname:
            return jsonify({
                'status': 400,
                'message': '缺少套件名称！',
                'data': data,
            })

        cname = data.get('cname', None)
        if not cname:
            return jsonify({
                'status': 400,
                'message': '缺少用例名称！',
                'data': data,
            })

        id = self.service.create(data)
        return jsonify({
            'status': 0,
            'message': 'success',
            'data': {
                'id': id
            },
        })

    @catch_exception
    def delete(self):
        data = request.get_json()

        sid = data.get('sid', None)
        if not sid:
            return jsonify({
                'status': 400,
                'message': '缺少套件ID！',
                'data': data,
            })

        cid = data.get('cid', None)
        if not cid:
            return jsonify({
                'status': 400,
                'message': '缺少用例ID！',
                'data': data,
            })

        count = self.service.delete(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': count,
        })

    @catch_exception
    def update(self):
        data = request.get_json()

        sid = data.get('sid', None)
        if not sid:
            return jsonify({
                'status': 400,
                'message': '缺少套件ID！',
                'data': data,
            })

        cid = data.get('cid', None)
        if not cid:
            return jsonify({
                'status': 400,
                'message': '缺少用例ID！',
                'data': data,
            })

        id = self.service.update(data)
        return jsonify({
            'status': 0,
            'message': 'success',
            'data': {
                'id': id
            },
        })

    @catch_exception
    def search(self):

        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        count, result = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'total': count,
        })
