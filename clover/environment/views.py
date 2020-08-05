
import traceback

from flask import request
from flask import jsonify

from clover.core import RESERVED
from clover.views import CloverView
from clover.environment.service import TeamService
from clover.environment.service import KeywordService
from clover.environment.service import VariableService


class TeamView(CloverView):

    def __init__(self):
        super(TeamView, self).__init__()
        self.service = TeamService()

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

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "无效的owner[{0}]参数！".format(data['owner']),
                'data': data
            })

        try:
            status = self.service.create(data)
            if status == 1:
                return jsonify({
                    'status': 400,
                    'message': '该团队与项目已存在，请更换',
                })
            else:
                return jsonify({
                    'status': 0,
                    'message': '创建团队项目成功',
                })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def delete(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "无效的id[{0}]参数！".format(data['id']),
                'data': data
            })

        try:
            id = self.service.detele(data)
            return jsonify({
                'status': 0,
                'message': '成功删除数据！',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "无效的id[{0}]参数！".format(data['id']),
                'data': data
            })

       try:
            status = self.service.update(data)
            if status == 1:
                return jsonify({
                    'status': 400,
                    'message': '该团队与项目已存在，请更换',

                })
            else:
                return jsonify({
                    'status': 0,
                    'message': 'ok',
                })
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):
        """
        :return:
        """
        data = request.values.to_dict()

        try:
            total, result = self.service.search(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def aggregate(self):
        """
        :return:
        """
        data = request.get_json()

        try:
            data = self.service.aggregate(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def navigation(self):
        """
        :return:
        """
        data = request.get_json()

        try:
            data = self.service.navigation(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': data
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })


class VariableView(CloverView):

    def __init__(self):
        super(VariableView, self).__init__()
        self.service = VariableService()

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

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "无效的owner[{0}]参数！".format(data['owner']),
                'data': data
            })

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': "无效的name[{0}]参数！".format(data['name']),
                'data': data
            })

        if data['name'] in RESERVED:
            return jsonify({
                'status': 400,
                'message': "请修改变量名，[{0}]是平台内置变量！".format(data['name']),
                'data': data
            })

        if 'value' not in data or not data['value']:
            return jsonify({
                'status': 400,
                'message': "无效的value[{0}]参数！".format(data['value']),
                'data': data
            })

        try:
            status = self.service.create(data)
            if not status:
                return jsonify({
                    'status': 0,
                    'message': '成功创建变量！',
                })
            else:
                return jsonify({
                    'status': 400,
                    'message': '此项目已有相同的变量名，请更换！',

                })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def delete(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "无效的id[{0}]参数！".format(data['id']),
                'data': data
            })

        try:
            id = self.service.detele(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "无效的id[{0}]参数！".format(data['id']),
                'data': data
            })

        try:
            status = self.service.update(data)
            if status == 1:
                return jsonify({
                    'status': 400,
                    'message': '此项目已有相同的变量名，请更换',

                })
            else:
                return jsonify({
                    'status': 0,
                    'message': 'ok',
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):
        """
        :return:
        """
        data = request.values.to_dict()

        try:
            total, result = self.service.search(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })


class KeywordView(CloverView):

    def __init__(self):
        super(KeywordView, self).__init__()
        self.service = KeywordService()

    def create(self):
        """
        :return:
        """
        data = request.get_json()

        if 'keyword' not in data or not data['keyword']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'description' not in data or not data['description']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少功能描述!',
                'data': data
            })

        try:
            result = self.service.create(data)
            return jsonify({
                'status': 0,
                'message': "创建关键字成功！",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def delete(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "删除关键字时缺少必要的ID",
                'data': data
            })

        try:
            id = self.service.delete(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def update(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "更新关键字时缺少必要的ID",
                'data': data
            })

        try:
            id = self.service.update(data)
            return jsonify({
                'status': 0,
                'message': '更新关键字成功！',
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def search(self):
        """
        :return:
        """
        data = request.get_json()

        try:
            total, result = self.service.search(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result,
                'total': total,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'traceback': traceback.format_stack(),
                'data': data
            })

    def debug(self):
        """
        :return:
        """
        data = request.get_json()

        if 'keyword' not in data or not data['keyword']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'expression' not in data or not data['expression']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少调用表达式!',
                'data': data
            })

        try:
            result = self.service.debug(data)
            return jsonify({
                'status': 0,
                'message': "关键字调试结束！",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })
