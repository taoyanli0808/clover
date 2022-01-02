
from flask import request
from flask import jsonify

from clover.core import RESERVED
from clover.views import CloverView
from clover.core.exception import catch_exception
from clover.environment.service import TeamService
from clover.environment.service import VariableService


class TeamView(CloverView):

    def __init__(self):
        super(TeamView, self).__init__()
        self.service = TeamService()

    @catch_exception
    def api_v1_team_create(self):
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

    @catch_exception
    def api_v1_team_delete(self):
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

        id = self.service.detele(data)
        print(id)
        1/0
        return jsonify({
            'status': 0,
            'message': '成功删除数据！',
            'data': id
        })

    @catch_exception
    def api_v1_team_update(self):
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

    @catch_exception
    def api_v1_team_search(self):
        """
        :return:
        """
        data = request.values.to_dict()

        total, result = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'total': total,
        })

    @catch_exception
    def api_v1_team_aggregate(self):
        """
        :return:
        """
        data = request.get_json()

        data = self.service.aggregate(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })

    @catch_exception
    def api_v1_team_navigation(self):
        """
        :return:
        """
        data = request.get_json()

        data = self.service.navigation(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': data
        })


class VariableView(CloverView):

    def __init__(self):
        super(VariableView, self).__init__()
        self.service = VariableService()

    @catch_exception
    def api_v1_variable_create(self):
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

    @catch_exception
    def api_v1_variable_delete(self):
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

        id = self.service.detele(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })

    @catch_exception
    def api_v1_variable_update(self):
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

    @catch_exception
    def api_v1_variable_search(self):
        """
        :return:
        """
        data = request.values.to_dict()

        total, result = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'total': total,
        })
