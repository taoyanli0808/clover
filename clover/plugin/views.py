
import traceback

from flask import request
from flask import jsonify

from clover.plugin.service import PluginService
from clover.views import CloverView


class PluginView(CloverView):

    def __init__(self):
        super(PluginView, self).__init__()
        self.service = PluginService()

    def create(self):
        """
        :return:
        """
        data = request.get_json()

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': "无效的team[{0}]参数！".format(data['team']),
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': "无效的project[{0}]参数！".format(data['project']),
                'data': data
            })

        if 'plugin' not in data or not data['plugin']:
            return jsonify({
                'status': 400,
                'message': "无效的plugin[{0}]参数！".format(data['plugin']),
                'data': data
            })

        try:
            id = self.service.create(data)
            return jsonify({
                'status': 0,
                'message': '成功创建插件！',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })
