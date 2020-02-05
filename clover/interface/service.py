#coding=utf-8

import datetime

from clover.exts import db
from clover.common.executor import Executor
from clover.common.tasks import interface_task

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.interface.models import InterfaceModel

from clover.report.service import ReportService


class InterfaceService(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        model = InterfaceModel(**data)
        db.session.add(model)
        db.session.commit()

        executor = Executor('debug')
        executor.execute([data], data)

        return model.id, executor.status, executor.message, data

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id_list = data.pop('id_list')
        for id in id_list:
            result = InterfaceModel.query.get(id)
            soft_delete(result)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = InterfaceModel.query.get(data['id'])
        if old_model is None:
            model = InterfaceModel(**data)
            db.session.add(model)
            db.session.commit()
            old_model = model
        else:
            old_model.team = data['team']
            old_model.project = data['project']
            old_model.name = data['name']
            old_model.method = data['method']
            old_model.host = data['host']
            old_model.path = data['path']
            old_model.header = data['header']
            old_model.params = data['params']
            old_model.body = data['body']
            old_model.verify = data['verify']
            old_model.extract = data['extract']
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        executor = Executor('debug')
        result = executor.execute([data], data)

        return old_model.id, executor.status, executor.message, result[0]

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        if 'team' in data and data['team']:
            filter.setdefault('team', data.get('team'))

        if 'project' in data and data['project']:
            filter.setdefault('project', data.get('project'))

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = InterfaceModel.query.filter_by(
            **filter
        ).order_by(
            InterfaceModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = InterfaceModel.query.filter_by(**filter).count()
        return count, results

    def trigger(self, data):
        """
        # 这里创建一个空report，然后使用celery异步运行任务，
        # 当celery执行完毕后使用空report的id更新报告。
        :param data:
        :return:
        """
        # 创建空的report并提交
        report_service = ReportService()
        report = report_service.empty_report(data)
        report = report.to_dict()

        # 通过接口传递过来的suite id来查询需要运行的接口。
        id = data.get('id')
        interface = InterfaceModel.query.get(id)
        cases = [interface.to_dict()]

        # 使用celery异步运行的接口任务。
        interface_task.delay(cases, data, report)

        return report
