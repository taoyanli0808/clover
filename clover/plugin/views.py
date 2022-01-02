
from flask import request
from flask import jsonify

from clover.views import CloverView
from clover.common import allowed_file
from clover.plugin.service import PluginService
from clover.core.exception import catch_exception


class PluginView(CloverView):

    def __init__(self):
        super(PluginView, self).__init__()
        self.service = PluginService()

    @catch_exception
    def api_v1_plugin_create(self):
        """
        :return:
        """
        data = request.values.to_dict()
        file = request.files.get('file')

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

        if 'file' not in request.files or not file.filename:
            return jsonify({
                'status': 400,
                'message': "上传的文件不能为空！",
                'data': data
            })

        if not allowed_file(file.filename):
            return jsonify({
                'status': 400,
                'message': "不支持的文件类型！",
                'data': data
            })

        result = self.service.create(data, file)
        return jsonify({
            'status': 0,
            'message': '使用插件创建接口完成！',
            'data': result
        })
