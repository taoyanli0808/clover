
import os
import datetime

from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import soft_delete
from clover.models import query_to_dict
from clover.common import friendly_datetime
from clover.report.models import ReportModel


class ReportService():

    def __init__(self):
        pass

    def create(self, data):
        """
        :param data:
        :return:
        """
        pass

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = ReportModel.query.get(data['id'])
        if old_model is None:
            model = ReportModel(**data)
            db.session.add(model)
            db.session.commit()
            old_model = model
        else:
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

        return old_model

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
            result = result.to_dict() if result else None
            result = friendly_datetime(result)

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

        # 暂时用笨方法删除列表页不需要展示的大量数据。
        for result in results:
            if 'detail' in result:
                result.pop('detail')

        return count, results

    def log(self, data):
        """
        :param data:
        :return:
        """
        log = '{}.log'.format(data.get('id', 0))
        path = os.path.join(os.getcwd(), 'logs')
        logs = os.listdir(path)
        if log not in logs:
            return {
                'status': 501,
                'message': '运行日志不存在！',
                'data': ''
            }
        name = os.path.join(os.getcwd(), 'logs', log)
        with open(name) as file:
            content = file.read()
        return {
            'status': 0,
            'message': '成功检索到日志！',
            'data': content
        }


    def empty_report(self, data):
        """
        :param data:
        :return:
        """
        name = data['report'] if 'report' in data and data['report'] else data.get('name')
        report = {
            'team': data['team'],
            'project': data['project'],
            'name': name,
            'type': 'interface',
            'interface': {
                'verify': 0,
                'passed': 0,
                'failed': 0,
                'error': 0,
                'sikped': 0,
                'total': 0,
                'percent': 0.0,
            },
            'start': datetime.datetime.now(),
            'end': datetime.datetime.now(),
            'duration': 0,
            'platform': {},
            'detail': 0,
            'log': {},
        }

        model = ReportModel(**report)
        db.session.add(model)
        try:
            db.session.commit()
            return model
        except ProgrammingError:
            return None
