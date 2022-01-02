from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.log.service import LogService
from clover.core.exception import catch_exception


class LogView(CloverView):

    def __init__(self):
        super(LogView, self).__init__()
        self.service = LogService()

    @catch_exception
    def api_v1_log_search(self):
        """
        :return:
        """
        data = request.get_json()

        id = data.get('id')
        if not id:
            return jsonify({
                'status': 400,
                'message': '缺少id参数！',
                'data': data,
            })

        logid = data.get('logid')
        if not logid:
            return jsonify({
                'status': 400,
                'message': '缺少logid参数！',
                'data': data,
            })

        count, results = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': '成功检索到{}条数据'.format(count),
            'data': results,
            'total': count
        })
