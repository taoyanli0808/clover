
import traceback

from flask import request
from flask import jsonify

from clover.environment.service import TeamService
from clover.environment.service import KeywordService
from clover.environment.service import VariableService
from clover.views import CloverView


class TeamView(CloverView):

    def __init__(self):
        super(TeamView, self).__init__()
<<<<<<< HEAD

    def create(self):

        data = request.get_json()

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter team[{0}]".format(data['team']),
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter project[{0}]".format(data['project']),
                'data': data
            })

        if 'owner' not in data or not data['owner']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter owner[{0}]".format(data['owner']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamcreate(data)
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

    def delete(self):

        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamdetele(data)
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

        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "invalid parameter id[{0}]".format(data['id']),
                'data': data
            })

        try:
            service = Service()
            id = service.Teamupdate(data)
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

        data = request.values.to_dict()

        try:
            service = Service()
            total, result = service.Teamsearch(data)
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

        data = request.get_json()

        try:
            service = Service()
            data = service.Teamaggregate(data)
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

    def debug(self):
        data = request.get_json()
        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Teamdebug(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

    def save(self):
        data = request.get_json()

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [mock]!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': 'invalid parameter [snippet]!',
                'data': data
            })

        try:
            service = Service()
            result = service.Teamsave(data)
            return jsonify({
                'status': 0,
                'message': "ok",
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': str(error),
                'data': data
            })

class VariableView(CloverView):

    def __init__(self):
        super(VariableView, self).__init__()
=======
        self.service = TeamService()
>>>>>>> remote_origin/master

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
<<<<<<< HEAD
            service = Service()
            id = service.Variabcreate(data)
=======
            id = self.service.create(data)
>>>>>>> remote_origin/master
            return jsonify({
                'status': 0,
                'message': '成功创建团队与项目！',
                'data': id
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
<<<<<<< HEAD
            service = Service()
            id = service.Variabdetele(data)
=======
            id = self.service.update(data)
>>>>>>> remote_origin/master
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

        if 'value' not in data or not data['value']:
            return jsonify({
                'status': 400,
                'message': "无效的value[{0}]参数！".format(data['value']),
                'data': data
            })

        try:
<<<<<<< HEAD
            service = Service()
            id = service.Variabupdate(data)
=======
            id = self.service.create(data)
>>>>>>> remote_origin/master
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
<<<<<<< HEAD
            service = Service()
            total, result = service.Variabsearch(data)
=======
            id = self.service.detele(data)
>>>>>>> remote_origin/master
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
<<<<<<< HEAD
            service = Service()
            data = service.Variabaggregate(data)
=======
            id = self.service.update(data)
>>>>>>> remote_origin/master
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


class KeywordView(CloverView):

    def __init__(self):
        super(KeywordView, self).__init__()
        self.service = KeywordService()

    def create(self):
        """
        :return:
        """
        data = request.get_json()

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '关键字需要定义名称!',
                'data': data
            })

        if 'snippet' not in data or not data['snippet']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少必要的测试数据!',
                'data': data
            })

        try:
<<<<<<< HEAD
            service = Service()
            result = service.Variabdebug(data)
=======
            result = self.service.create(data)
>>>>>>> remote_origin/master
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

        if 'mock' not in data or not data['mock']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少必要的测试数据!',
                'data': data
            })

        try:
<<<<<<< HEAD
            service = Service()
            result = service.Variabsave(data)
=======
            result = self.service.debug(data)
>>>>>>> remote_origin/master
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

