
from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import query_to_dict, soft_delete
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel
from clover.common.utils import get_mysql_error
from clover.common.executor import Executor


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

        results = SuiteModel.query.filter_by(**filter).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = SuiteModel.query.filter_by(**filter).count()
        return count, results

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        # ！attention 这里用例的执行顺序有保障么？
        # 查询出所有需要运行的用例
        cases = db.session.query(
            InterfaceModel
        ).filter(
            InterfaceModel.id.in_(tuple(data['cases']))
        ).all()
        cases = query_to_dict(cases)
        # 执行用例并获得运行结果
        executor = Executor()
        result = executor.execute(cases)
        return result
