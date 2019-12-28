
import re
import json
import datetime

from clover.common.utils.mongo import Mongo
from clover.common.utils import get_friendly_id
from clover.common.utils.mysqltools import MysqlHelper


class Service():

    def __init__(self):
        self.db = Mongo()
        self.mydb = MysqlHelper()

    def create(self, data):
        """
        :param data:
        :return:
        """
        # data.setdefault('_id', get_friendly_id())
        # data.setdefault('created', datetime.datetime.now())
        # collection = data.pop("type", None)
        # return self.db.insert("environment", collection, data)
        # mysql
        data.setdefault('uuid', get_friendly_id())
        data.setdefault('table', 'environment')
        data.pop('type', None)
        results = self.mydb.insert(data)
        return results

    def detele(self, data):
        """
        :param data:
        :return:
        """
        count = 0
        collection = data.get("type", None)
        print(data)
        for id in data['id_list']:
            result = self.db.delete("environment", collection, {'_id': id})
            count += result
        return count

    def update(self, data):
        """
        :param data:
        :return:
        """
        print(data)
        # filter = {'_id': data.pop('_id')}
        # collection = data.pop("type", None)
        # return self.db.update("environment", collection, filter, data)
        # mysql
        data.pop('type', None)
        filter = {'uuid': data.pop('_id')}
        data.setdefault('table', 'environment')
        results = self.mydb.update(data, filter)
        return results

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
        # cascader: 按照element ui库cascader需要的数据格式返回数据。
        #           团队和项目配置数据不会特别多，因此无需过多关注性能。
        :param data:
        :return:
        """
        if 'cascader' in data:
            cascader = {}
            _, results = self.db.search("environment", "team", {})
            for result in results:
                if result['team'] not in cascader:
                    cascader.setdefault(result['team'], {
                        'label': result['team'],
                        'value': result['team'],
                        'children': [{
                            'label': result['project'],
                            'value': result['project']
                        }],
                    })
                else:
                    labels = [item['label'] for item in cascader[result['team']]['children']]
                    if result['project'] not in labels:
                        cascader[result['team']]['children'].append({
                            'label': result['project'],
                            'value': result['project']
                        })
            return list(cascader.values())
        elif 'type' in data:
            collection = data.pop("type", None)
            key = data.pop("key", None)
            pipeline = [
                {'$group': {'_id': "$" + key}},
            ]
            result = self.db.aggregate("environment", collection, pipeline)
            return result
        else:
            return []

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


if __name__ == '__main__':
    service = Service()
    print(service.aggregate({'cascader': None}))
