#coding=utf-8

import datetime

from clover.exts import db
from clover.core.message import Message
from clover.core.executor import Executor

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.interface.models import InterfaceModel


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
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        executor = Executor('debug')
        executor.execute([data], data)

        return old_model.id, executor.status, executor.message, data

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = InterfaceModel.query.get(data['id'])
            count = 1 if result else 0
            result = result.to_dict() if result else None
            return count, result

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
        # 通过接口传递过来的suite id来查询需要运行的接口。
        id = data.get('id')
        interface = InterfaceModel.query.get(id)

        # 如果不存在接口则直接返回
        if not interface:
            return

        cases = [interface.to_dict()]

        message = Message()
        message.send({'case': cases, 'data': data})

        return
