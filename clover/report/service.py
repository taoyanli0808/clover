
import datetime

from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import soft_delete
from clover.common import friendly_datetime
from clover.report.models import ReportModel
from clover.core.exception import catch_database_exception


class ReportService():

    def __init__(self):
        pass

    @catch_database_exception
    def create(self, data):
        """
        :param data:
        :return:
        """
        model = ReportModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.to_dict()

    @catch_database_exception
    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        old_model = ReportModel.query.get(data.get('id'))
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

    @catch_database_exception
    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        result = ReportModel.query.get(id)
        soft_delete(result)

    @catch_database_exception
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

        results = ReportModel.query.with_entities(
            ReportModel.id, ReportModel.team, ReportModel.project,
            ReportModel.name, ReportModel.type, ReportModel.interface,
            ReportModel.duration, ReportModel.start, ReportModel.end
        ).filter_by(
            **filter
        ).order_by(
            ReportModel.created.desc()
        ).offset(offset).limit(limit)

        results = [{
            'id': result.id,
            'team': result.team,
            'project': result.project,
            'name': result.name,
            'type': result.type,
            'duration': result.duration,
            'interface': result.interface,
            'start': result.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': result.end.strftime('%Y-%m-%d %H:%M:%S'),
        } for result in results]

        # 报告新增跳过兼容1.0版本，历史数据为null,兼容历史数据拼错的skiped字段
        for result in results:
            if 'sikped' in result['interface']:
                result['interface'].update({'skiped': result['interface'].pop("sikped")})

        count = ReportModel.query.filter_by(**filter).count()

        return count, results

    def log(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        report = ReportModel.query.get(id)
        return report.log
