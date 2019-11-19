
import re
import json

from common.utils.mongo import Mongo


class Service():

    def __init__(self):
        self.db = Mongo()

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
        :param data:
        :return:
        """
        # 这里需要先提取函数名，然后关键字用函数名进行索引，存到数据库。
        # 如果数据库中函数名已经存在怎么办，是否需要先查询，重复则失败？
        self.db.insert()
        return data
