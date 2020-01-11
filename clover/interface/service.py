#coding=utf-8

import time

from clover.exts import db
from clover.models import query_to_dict
from clover.interface.models import InterfaceModel
from clover.common.interface.executor import Executor


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
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id_list = data.pop('id_list')
        for id in id_list:
            result = InterfaceModel.query.get(id)
            db.session.delete(result)
            db.session.commit()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {}

        if 'team' in data and data['team']:
            filter.setdefault('team', data.get('team'))

        if 'owner' in data and data['owner']:
            filter.setdefault('owner', data.get('owner'))

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = InterfaceModel.query.filter_by(**filter).offset(offset).limit(limit)
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
        run_id = 111
        id = data.get('id')
        model = InterfaceModel.query.get(id)
        case = model.to_dict()
        # 运行测试用例，注意execute的参数是list。
        executor = Executor()
        result = executor.execute([case])
        print(result)
        return run_id
