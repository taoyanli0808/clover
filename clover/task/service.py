
import datetime

from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.common import get_mysql_error

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.task.models import TaskModel


class TaskService():

    def __init__(self):
        pass

    def create(self, data):
        """
        :param data:
        :return:
        """
        model = TaskModel(**data)
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
        id = data.pop('id')

        ids = [id] if isinstance(id, (int, str,)) else list(id)

        for id in ids:
            result = TaskModel.query.get(id)
            soft_delete(result)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = TaskModel.query.get(data['id'])
        if old_model is None:
            model = TaskModel(**data)
            db.session.add(model)
            db.session.commit()
        else:
            old_model.team = data['team']
            old_model.project = data['project']
            old_model.name = data['name']
            old_model.cron = data['cron']
            old_model.variable = data['variable']
            old_model.updated = datetime.datetime.now()
            db.session.commit()

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

        results = TaskModel.query.filter_by(
            **filter
        ).order_by(
            TaskModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = TaskModel.query.filter_by(**filter).count()
        return count, results

    def trigger(self, data):
        """
        # 这里创建一个空report，然后使用celery异步运行任务，
        # 当celery执行完毕后使用空report的id更新报告。
        :param data:
        :return:
        """
        # 创建空的report并提交
        # report_service = ReportService()
        # report = report_service.empty_report(data)
        # report = report.to_dict()
        #
        # # 通过接口传递过来的suite id来查询需要运行的接口。
        # id = data.get('id')
        # suite = SuiteModel.query.get(id)
        # cases = db.session.query(
        #     InterfaceModel
        # ).filter(
        #     InterfaceModel.id.in_(suite.cases)
        # ).all()
        # cases = query_to_dict(cases)
        #
        # # 使用celery异步运行的接口任务。
        # interface_task.delay(cases, data, report)
        #
        # return report
        pass
