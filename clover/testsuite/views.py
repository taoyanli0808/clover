
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.testsuite.service import Service


class TestSuiteView(CloverView):

    def __init__(self):
        super(TestSuiteView, self).__init__()

    def create(self):
        data = request.get_json()

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
        pass

    def update(self):
        pass

    def search(self):
        pass
