import datetime

from clover.exts import db


def query_to_dict(results):
    """
    # 将BaseQuery对象转换为可以json序列化的普通python对象。
    # 通常采用Model.query方法返回的数据需要使用次方法转换。
    # 注意，如果只返回一条数据直接调用to_dict方法即可。
    :param results:
    :return:
    """
    results = list(map(lambda x: x.to_dict(), results))
    # results = list(x for x in results if x['enable'] == 0)
    for result in results:
        result['created'] = result['created'].strftime('%Y-%m-%d %H:%M:%S')
        result['updated'] = result['updated'].strftime('%Y-%m-%d %H:%M:%S')
        if 'start' in result:
            result['start'] = result['start'].strftime('%Y-%m-%d %H:%M:%S')
        if 'end' in result:
            result['end'] = result['end'].strftime('%Y-%m-%d %H:%M:%S')
    return results


def soft_delete(model):
    """
    :param model:
    :return:
    """
    # db.session.delete(model)
    # db.session.commit()
    model.enable = 1
    model.updated = datetime.datetime.now()
    db.session.commit()


class CloverModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
