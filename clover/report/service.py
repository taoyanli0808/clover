
import datetime

from clover.exts import db
from clover.models import soft_delete
from clover.common import friendly_datetime
from clover.report.models import ReportModel


class ReportService(object):

    def create(self, data):
        """
        :param data:
        :return:
        """
        model = ReportModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

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

        if 'name' in data and data['name']:
            results = ReportModel.query.with_entities(
                ReportModel.id, ReportModel.team, ReportModel.project,
                ReportModel.name, ReportModel.type, ReportModel.interface,
                ReportModel.duration, ReportModel.start, ReportModel.end,
                ReportModel.logid
            ).filter_by(
                **filter
            ).filter(
                ReportModel.name.like('%' + data['name'] + '%')
            ).order_by(
                ReportModel.created.desc()
            ).offset(offset).limit(limit)
        else:
            results = ReportModel.query.with_entities(
                ReportModel.id, ReportModel.team, ReportModel.project,
                ReportModel.name, ReportModel.type, ReportModel.interface,
                ReportModel.duration, ReportModel.start, ReportModel.end,
                ReportModel.logid
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
            'logid': result.logid,
            'start': result.start.strftime('%Y-%m-%d %H:%M:%S'),
            'end': result.end.strftime('%Y-%m-%d %H:%M:%S'),
        } for result in results]

        if 'name' in data and data['name']:
            count = ReportModel.query.filter_by(**filter).filter(
                ReportModel.name.like('%' + data['name'] + '%')
            ).count()
        else:
            count = ReportModel.query.filter_by(**filter).count()

        return count, results
