#coding=utf-8

import datetime

from sqlalchemy import and_

from clover.exts import db

from clover.models import soft_delete
from clover.models import query_to_dict
from clover.history.models import HistoryModel


class HistoryService(object):

    def create(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        model = HistoryModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.sid, model.cid

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.pop('id')
        result = HistoryModel.query.get(id)
        soft_delete(result)

    def update(self, data):
        """
        # 使用id作为条件，更新数据库重的数据记录。
        # 通过id查不到数据时增作为一条新的记录存入。
        :param data:
        :return:
        """
        model = HistoryModel.query.filter(
            and_(HistoryModel.sid == data['sid'], HistoryModel.cid == data['cid'])
        ).first()
        {setattr(model, k, v) for k, v in data.items()}
        model.updated = datetime.datetime.now()
        db.session.commit()
        return model.sid, model.cid

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if ('sid' in data and data['sid']) and ('cid' in data and data['cid']):
            filter.setdefault('sid', data.get('sid'))
            filter.setdefault('cid', data.get('cid'))
            result = HistoryModel.query.filter(
                and_(HistoryModel.sid == data['sid'], HistoryModel.cid == data['cid'])
            ).first()
            count = 1 if result else 0
            result = result.to_dict() if result else None
            return count, result

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

        results = HistoryModel.query.filter_by(
            **filter
        ).order_by(
            HistoryModel.created.desc()
        ).offset(offset).limit(limit)

        results = query_to_dict(results)
        count = HistoryModel.query.filter_by(**filter).count()

        return count, results
