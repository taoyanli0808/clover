
from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import query_to_dict
from clover.testsuite.models import SuiteModel
from clover.common.utils import get_mysql_error


class Service():

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

        results = SuiteModel.query.filter_by(**filter).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = SuiteModel.query.filter_by(**filter).count()
        return count, results

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        for case in data['cases']:
            _, result = self.db.search("interface", "case", {'_id': case['_id']})
            print(result)
