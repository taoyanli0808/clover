
import datetime

from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.core.producer import Producer
from clover.common import get_mysql_error

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel


class SuiteService():

    def __init__(self):
        pass

    def create(self, data):
        """
        :param data:
        :return:
        """
        model = SuiteModel(**data)
        db.session.add(model)
        # 这是一个处理数据库异常的例子，后面最好有统一的处理方案。
        try:
            db.session.commit()
        except ProgrammingError as error:
            code, msg = get_mysql_error(error)
            return (code, msg)
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id_list = data.pop('id_list')
        for id in id_list:
            result = SuiteModel.query.get(id)
            soft_delete(result)

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

        results = SuiteModel.query.filter_by(
            **filter
        ).order_by(
            SuiteModel.created.desc()
        ).offset(offset).limit(limit)

        results = query_to_dict(results)

        # 禁用功能兼容1.0版本，历史数据为null
        for result in results:
            if result['status'] == None:
                result['status'] = True

        count = SuiteModel.query.filter_by(**filter).count()

        return count, results

    def trigger(self, data):
        """
        # 这里创建一个空report，然后使用celery异步运行任务，
        # 当celery执行完毕后使用空report的id更新报告。
        :param data:
        :return:
        """

        producer = Producer()
        producer.send({
            'type': 'suite',
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
        old_model = SuiteModel.query.get(data['id_list'])
        {setattr(old_model, k, v) for k, v in data.items()}
        old_model.updated = datetime.datetime.now()
        db.session.commit()
        return