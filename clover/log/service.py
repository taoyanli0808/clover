
from clover.exts import db
from clover.core.log import Log
from clover.models import soft_delete
from clover.models import query_to_dict
from clover.log.models import LogModel


class LogService(object):

    def create(self, data):
        """
        :param data:
        :return:
        """
        if isinstance(data, Log):
            data = data.log

        model = LogModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        result = LogModel.query.get(id)
        soft_delete(result)

    def search(self, data):
        """
        :param data:
        :return:
        """
        report_id = data.get('id')
        logid = data.get('logid')

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 100))
        except TypeError:
            limit = 10

        results = LogModel.query.filter(
            LogModel.report_id==report_id, LogModel.enable==0
        ).order_by(
            LogModel.created.desc()
        ).offset(offset).limit(limit)

        results = query_to_dict(results)

        count = LogModel.query.filter(
            LogModel.report_id==report_id, LogModel.enable==0
        ).count()

        return count, results
