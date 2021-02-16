
import datetime

from clover.exts import db

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.mock.models import MockModel


class MockService(object):

    def __init__(self): pass

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        model = MockModel(**data)
        db.session.add(model)
        db.session.commit()

        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.pop('id')
        result = MockModel.query.get(id)
        soft_delete(result)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = MockModel.query.get(data['id'])
        if old_model is None:
            model = MockModel(**data)
            db.session.add(model)
            db.session.commit()
            old_model = model
        else:
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        return old_model.id

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = MockModel.query.get(data['id'])
            count = 1 if result else 0
            result = result.to_dict() if result else None
            return count, result

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = MockModel.query.filter_by(
            **filter
        ).order_by(
            MockModel.created.desc()
        ).offset(offset).limit(limit)

        results = query_to_dict(results)

        count = MockModel.query.filter_by(**filter).count()

        return count, results