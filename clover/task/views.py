
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.task.service import TaskService


class TaskView(CloverView):

    def __init__(self):
        super(TaskView, self).__init__()
        self.service = TaskService()

    def create(self):
        data = request.get_json()

        if 'team' not in data or not data['team']:
            return jsonify({
                'status': 400,
                'message': '请选择团队！',
                'data': data
            })

        if 'project' not in data or not data['project']:
            return jsonify({
                'status': 400,
                'message': '请选择项目！',
                'data': data
            })

        if 'name' not in data or not data['name']:
            return jsonify({
                'status': 400,
                'message': '请求缺少任务名称！',
                'data': data
            })

        if 'cron' not in data or not data['cron']:
            return jsonify({
                'status': 400,
                'message': '请求缺少调度表达式！',
                'data': data
            })

        try:
            id = self.service.create(data)
            return jsonify({
                'status': 0,
                'message': '创建定时任务成功，ID[{}]'.format(id),
                'data': id
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '创建定时任务发生异常，请联系管理员！',
                'data': str(error)
            })

    def delete(self):
        data = request.get_json()

        if 'id_list' not in data or not data['id_list']:
            return jsonify({
                'status': 400,
                'message': '请选择您要删除的接口！',
                'data': data
            })

        try:
            count = self.service.delete(data)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': count,
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '服务器出错，请联系管理员！',
                'data': data
            })

    def update(self):
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': '请选择您要更新的定时任务！',
                'data': data
            })

        try:
            results = self.service.update(data)
            return jsonify({
                'status': 0,
                'message': '更新定时任务数据成功',
                'data': results
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '检索异常，请联系管理员！',
                'data': str(error)
            })

    def search(self):
        if request.method == 'GET':
            data = request.values.to_dict()
        else:
            data = request.get_json()

        try:
            count, results = self.service.search(data)
            return jsonify({
                'status': 0,
                'message': '成功检索到{}条数据'.format(count),
                'data': results,
                'total': count
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '检索异常，请联系管理员！',
                'data': str(error)
            })

    def trigger(self):
        """
        :param data:
        :return:
        """
        data = request.get_json()

        if 'cases' not in data or not data['cases']:
            return jsonify({
                'status': 400,
                'message': '请求缺少cases参数！',
                'data': data
            })

        try:
            result = self.service.trigger(data)
            return jsonify({
                'status': 0,
                'message': '运行测试套件[{0}]成功，测试报告ID[{1}]'.format(id, result),
                'data': result
            })
        except Exception as error:
            return jsonify({
                'status': 500,
                'message': '运行套件出错，请联系管理员！',
                'data': str(error)
            })
