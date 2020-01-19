
from flask import jsonify

from clover.views import CloverView
from clover.common import get_system_info
from clover.common import get_python_dependency
from clover.common import get_nodejs_dependency
from clover.index.service import Service


class IndexView(CloverView):

    def __init__(self):
        super(IndexView, self).__init__()
        self.service = Service()

    def info(self):
        """
        :param data:
        :return:
        """
        try:
            info = {
                **get_system_info(),
                'python-dependency': get_python_dependency(),
                'nodejs-dependency': get_nodejs_dependency()
            }
            return jsonify({
                'status': 0,
                'message': 'clover平台版本与依赖信息。',
                'data': info
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '运行出错，请联系管理员！',
                'data': str(error)
            })

    def count(self):
        """
        :param data:
        :return:
        """
        try:
            count = self.service.count()
            return jsonify({
                'status': 0,
                'message': 'clover平台数据统计。',
                'data': count
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '运行出错，请联系管理员！',
                'data': str(error)
            })
