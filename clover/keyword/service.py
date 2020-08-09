
import datetime

from clover.exts import db
from clover.core.keyword import Keyword
from clover.models import query_to_dict, soft_delete
from clover.keyword.models import KeywordModel


class KeywordService(object):

    def create(self, data):
        """
        # 暂时没有前端页面 -- SQL暂时不更换
        # 这里需要先提取函数名，然后关键字用函数名进行索引，存到数据库。
        # 如果数据库中函数名已经存在怎么办，是否需要先查询，重复则失败？
        :param data:
        :return:
        """
        keyword = data.get('keyword')
        description = data.get('description')

        # 执行关键字提取函数名称
        _keyword = Keyword(keyword)
        function_name = _keyword.get_function_name_from_source()

        data = {
            'name': function_name,
            'description': description,
            'keyword': keyword
        }

        model = KeywordModel(**data)
        db.session.add(model)
        db.session.commit()
        return model.id

    def delete(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        model = KeywordModel.query.get(id)
        if model is not None:
            soft_delete(model)

    def update(self, data):
        """
        :param data:
        :return:
        """
        id = data.get('id')
        old_model = KeywordModel.query.get(id)
        if old_model is None:
            model = KeywordModel(**data)
            db.session.add(model)
            db.session.commit()
        else:
            {setattr(old_model, k, v) for k, v in data.items()}
            old_model.updated = datetime.datetime.now()
            db.session.commit()

    def search(self, data):
        """
        :param data:
        :return:
        """
        filter = {'enable': 0}

        # 如果按照id查询则返回唯一的数据或None
        if 'id' in data and data['id']:
            filter.setdefault('id', data.get('id'))
            result = KeywordModel.query.get(data['id'])
            count = 1 if result else 0
            result = result.to_dict() if result else None
            return count, result

        try:
            offset = int(data.get('offset', 0))
        except TypeError:
            offset = 0

        try:
            limit = int(data.get('limit', 10))
        except TypeError:
            limit = 10

        results = KeywordModel.query.filter_by(**filter) \
            .offset(offset).limit(limit)
        results = query_to_dict(results)
        count = KeywordModel.query.filter_by(**filter).count()
        return count, results

    def debug(self, data):
        """
        # 自定义关键字中提取函数名和参数，在后面拼接出调用请求，
        # 最后交给exec函数执行，如果提取函数名和参数失败则不处理。
        :param data:
        :return:
        """
        keyword = data.get('keyword')
        expression = data.get('expression')
        _keyword = Keyword(keyword)
        _keyword.is_keyword(expression)
        result = _keyword.execute()
        return result
