#coding=utf-8

import datetime

from clover.exts import db

from clover.models import query_to_dict
from clover.dashboard.models import DashboardModel


class DashboardService(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        try:
            model = DashboardModel(**data)
            db.session.add(model)
            db.session.commit()

            return model.id
        except:
            db.rollback()

    def update(self, data):
        """
        # Use ID as a condition to update the database's duplicate data records.
        # If no data can be found through ID, it will be added as a new record.
        :param data:
        :return:
        """
        try:
            old_model = DashboardModel.query.get(data['id'])
            if old_model is None:
                model = DashboardModel(**data)
                db.session.add(model)
                db.session.commit()
                return model.id
            else:
                {setattr(old_model, k, v) for k, v in data.items()}
                # old_model.team = data['team']
                # old_model.project = data['project']
                # old_model.name = data['name']
                # old_model.method = data['method']
                # old_model.host = data['host']
                # old_model.path = data['path']
                # old_model.header = data['header']
                # old_model.params = data['params']
                # old_model.body = data['body']
                # old_model.verify = data['verify']
                # old_model.extract = data['extract']
                old_model.updated = datetime.datetime.now()
                db.session.commit()

                return old_model.id
        except:
            db.rollback()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0, **data}

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = DashboardModel.query.filter_by(
            **filter
        ).order_by(
            DashboardModel.created.desc()
        ).offset(offset).limit(limit)
        results = query_to_dict(results)
        count = DashboardModel.query.filter_by(**filter).count()
        return count, results
