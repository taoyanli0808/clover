
from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import query_to_dict, soft_delete
from clover.report.models import ReportModel


class Service():

    def __init__(self):
        pass

    def create(self, data):
        """
        :param data:
        :return:
        """
        pass

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        result = ReportModel.query.get(id)
        soft_delete(result)

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = ReportModel.query.get(data['id'])
            count = 1 if result else 0
            result = query_to_dict([result])[0] if result else None

            return count, result

        # 普通查询配置查询参数
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

        results = ReportModel.query.filter_by(
            **filter
        ).order_by(
            ReportModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = ReportModel.query.filter_by(**filter).count()
        return count, results
