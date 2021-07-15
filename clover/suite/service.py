
import datetime


from clover.exts import db
from clover.core.producer import Producer

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.suite.models import SuiteModel


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
        db.session.commit()
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

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = SuiteModel.query.get(data['id'])
        if old_model is None:
            model = SuiteModel(**data)
            db.session.add(model)
            db.session.commit()
            old_model = model
        else:
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        return old_model.to_dict()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = SuiteModel.query.get(data['id'])
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

        if 'caseName' in data and data['caseName']:
            results = SuiteModel.query.filter_by(
                **filter
            ).filter(
                SuiteModel.name.like('%' + data['caseName'] + '%')
            ).order_by(
                SuiteModel.created.desc()
            ).offset(offset).limit(limit)
        else:
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

        if 'caseName' in data and data['caseName']:
            count = SuiteModel.query.filter_by(**filter).filter(
                SuiteModel.name.like('%' + data['caseName'] + '%')
            ).count()
        else:
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
            'name': data.get('name'),
            'variable': data,
            'trigger': data.get('trigger', 'clover'),
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
