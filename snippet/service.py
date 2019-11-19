
import re
import json

class Service():

    def __init__(self):
        pass

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
        return data
