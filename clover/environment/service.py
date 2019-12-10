
import re
import json
import datetime

from clover.common.utils.mongo import Mongo
from clover.common.utils import get_friendly_id


class Service():

    def __init__(self):
        self.db = Mongo()

    def create(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('_id', get_friendly_id())
        data.setdefault('created', datetime.datetime.now())
        collection = data.get("type", None)
        return self.db.insert("environment", collection, data)

    def detele(self, data):
        """
        :param data:
        :return:
        """
        count = 0
        collection = data.get("type", None)
        for id in data['id_list']:
            result = self.db.delete("environment", collection, {'_id': id})
            count += result
        return count

    def update(self, data):
        """
        :param data:
        :return:
        """
        filter = {'_id': data.pop('_id')}
        collection = data.get("type", None)
        return self.db.update("environment", collection, filter, data)

    def search(self, data):
        """
        :param data:
        :return:
        """
        collection = data.pop("type", None)
        total, result = self.db.search("environment", collection, data)
        for r in result:
            r['created'] = r['created'].strftime("%Y-%m-%d %H:%M:%S")
        return total, result

    def aggregate(self, data):
        """
        :param data:
        :return:
        """
        collection = data.pop("type", None)
        key = data.pop("key", None)
        pipeline = [
            {'$group': {'_id': "$" + key}},
        ]
        return self.db.aggregate("environment", collection, pipeline)

    def debug(self, data):
        """
        # 自定义关键字中提取函数名和参数，在后面拼接出调用请求，
        # 最后交给exec函数执行，如果提取函数名和参数失败则不处理。
        :param data:
        :return:
        """
        mock = json.loads(data.get('mock'))
        snippet = data.get('snippet')
        func = re.findall(r'def\s+(.+?):', snippet)
        if func:
            snippet += '\n' + func[0]
            exec(snippet, {'data': mock})
        return mock

    def save(self, data):
        """
        # 这里需要先提取函数名，然后关键字用函数名进行索引，存到数据库。
        # 如果数据库中函数名已经存在怎么办，是否需要先查询，重复则失败？
        :param data:
        :return:
        """
        mock = json.loads(data.get('mock'))
        snippet = data.get('snippet')
        func = re.findall(r'def\s+(.+?)\(', snippet)
        name = func[0] if func else ""
        print({
            'name': name,
            'mock': mock,
            'snippet': snippet,
        })
        result = self.db.insert("environment", "snippet", {
            '_id': get_friendly_id(),
            'name': name,
            'mock': mock,
            'snippet': snippet,
        })
        print(result)
        return result
