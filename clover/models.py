
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
    for result in results:
        result['created'] = result['created'].strftime('%Y-%m-%d %H:%M:%S')
        result['updated'] = result['updated'].strftime('%Y-%m-%d %H:%M:%S')
    return results


class CloverModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
