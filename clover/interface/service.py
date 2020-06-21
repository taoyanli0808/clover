#coding=utf-8

import copy
import datetime

from clover.exts import db
from clover.core.context import Context
from clover.core.producer import Producer
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

        context = Context()
        context.build_context({
            'type': 'interface',
            'id': model.id,
            'user': data
        })
        executor = Executor('debug')
        status, message, data = executor.execute(context)

        return model.id, status, message, data

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

        context = Context()
        context.build_context({
            'type': 'interface',
            'id': data['id'],
            'user': data
        })
        executor = Executor('debug')
        status, message, data = executor.execute(context)

        return old_model.id, status, message, data

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
        :param data:
        :return:
        """
        producer = Producer()
        producer.send_stream({
            'type': 'interface',
            'sub_type': 'interface',
            'id': data.get('id'),
            'user': data,
        })
        return

    def switch(self,data):
        """
        :param data:
        :return:
        """
        old_model = InterfaceModel.query.get(data['id_list'])
        {setattr(old_model, k, v) for k, v in data.items()}
        old_model.updated = datetime.datetime.now()
        db.session.commit()
        return