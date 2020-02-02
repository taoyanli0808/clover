#coding=utf-8

import datetime

from clover.exts import db
from clover.models import query_to_dict, soft_delete
from clover.interface.models import InterfaceModel
from clover.common.executor import Executor


class Service(object):

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
        result = executor.execute([data], data)

        return model.id, executor.status, executor.message, result[0]

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
        :param data:
        :return:
        """
        # 需要通过case_id先查询到数据库里的测试用例。
        # run_id是一次运行的记录，查测试报告时使用。
        id = data.get('id')
        model = InterfaceModel.query.get(id)
        case = model.to_dict()
        # 运行测试用例，注意execute的参数是list。
        executor = Executor()
        result = executor.execute([case], data)
        return executor.status, executor.message, result
