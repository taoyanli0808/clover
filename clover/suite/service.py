
from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.common import get_mysql_error
from clover.common.tasks import interface_task

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.suite.models import SuiteModel
from clover.interface.models import InterfaceModel

from clover.report.service import ReportService


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
        count = SuiteModel.query.filter_by(**filter).count()
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
        suite = SuiteModel.query.get(id)

        # 如果不存在套件，则直接返回。
        if not suite:
            return

        # 创建空的report并提交
        if 'team' not in data or not data['team']:
            data['team'] = suite.team
        if 'project' not in data or not data['project']:
            data['project'] = suite.team
        report_service = ReportService()
        report = report_service.empty_report(data)
        report = report.to_dict()

        cases = [InterfaceModel.query.get(case).to_dict() for case in suite.cases]

        # 使用celery异步运行的接口任务。
        interface_task.apply_async(args=(cases, data, report))
        return report.get('id')
