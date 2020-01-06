
from clover.exts import db
from clover.models import query_to_dict
from clover.testsuite.models import SuiteModel


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
        db.session.commit()
        return model.id

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
