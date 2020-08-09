
from flask import jsonify

from clover import config

from clover.views import CloverView
from clover.common import get_system_info
from clover.common import get_python_dependency
from clover.index.service import Service
from clover.core.exception import catch_view_exception


class IndexView(CloverView):

    def __init__(self):
        super(IndexView, self).__init__()
        self.service = Service()

    @catch_view_exception
    def info(self):
        """
        :param data:
        :return:
        """
        info = {
            **get_system_info(),
            'python-dependency': get_python_dependency()
        }
        return jsonify({
            'status': 0,
            'message': 'clover平台版本与依赖信息。',
            'data': info
        })

    @catch_view_exception
    def count(self):
        """
        :param data:
        :return:
        """
        count = self.service.count()
        return jsonify({
            'status': 0,
            'message': 'clover平台数据统计。',
            'data': count
        })

    @catch_view_exception
    def config(self):
        return jsonify({
            'status': 0,
            'message': 'clover平台功能配置。',
            'data': config.MODULE
        })
