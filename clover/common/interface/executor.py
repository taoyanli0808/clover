
import json

import requests

from flask import g

from clover.common.utils.helper import derivation
from clover.common.interface.expect import Expect
from clover.environment.models import VariableModel


class Executor():

    def __init__(self):
        g.data = []

    def replace_variable(self, data):
        """
        # 这里对请求数据进行变量替换，将变量替换为具体值。
        # 变量和其值可以在"配置管理 -> 全局变量"里设置。
        # 目前支持host，header与param的变量替换。
        # 变量与值存储使用团队与项目进行区分，不同的团队与项目允许出现同名变量。
        :param data:
        :return:
        """
        filter = {
            'team': data.get('team'),
            'project': data.get('project')
        }
        results = VariableModel.query.filter_by(**filter).all()
        results.extend(g.data)

        data['host'] = derivation(data.get('host'), results)
        data['path'] = derivation(data.get('path'), results)

        if 'header' in data:
            for header in data['header']:
                header['key'] = derivation(header['key'], results)

        if 'params' in data:
            for param in data['params']:
                param['key'] = derivation(param['key'], results)

        return data

    def make_request(self, data):
        """
        :param data:
        :return:
        """
        print(data)
        # 发送http请求
        method = data.get("method")
        host = data.get("host")
        path = data.get("path")
        header = data.get('header', {})
        payload = data.get('params', {})
        url = host + path

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if header:
            header = {item['key']: item['value'] for item in header if item['key']}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if payload:
            payload = {item['key']: item['value'] for item in payload}

        if method == 'get':
            response = requests.request(method, url, params=payload, headers=header)
        else:
            response = requests.request(method, url, data=payload, headers=header)

        # 这里将响应的状态码，头信息和响应体单独存储，后面断言或提取变量会用到
        data['response'] = {
            'status': response.status_code,
            'header': dict(response.headers),
            'content': response.text
        }

        # 框架目前只支持json数据，在这里尝试进行json数据转换
        try:
            data['response']['json'] = json.loads(data['response']['content'])
        except Exception:
            data['response']['json'] = {}

        return data

    def convert_format(self, data):
        """
        # 这个函数暂时保留，如有必要，用于后续讲xml等其它格式数据进行转换。
        :param data:
        :return:
        """
        return data

    def execute_assertion(self, data):
        """
        :param data:
        :return:
        """
        expect = Expect(data)
        expect.test()
        return data

    def extract_variables(self, data):
        """
        :param data:
        :return:
        """
        if 'extract' not in data or not data['extract']:
            return data

        for extract in data['extract']:
            sel = extract['selector']
            expr = extract['expression']
            name = extract['expected']
            # 从这里开始使用分隔符取数据
            tmp = data['response']['json']
            for item in expr.split('.'):
                try:
                    item = int(item)
                    tmp = tmp[item]
                except ValueError:
                    tmp = tmp.get(item, None)
                    if tmp is None:
                        break
            g.data.append({'name': name, 'value': tmp})

        return data

    def record_result(self, data):
        """
        :param data:
        :return:
        """
        # data['_id'] = get_friendly_id()
        # self.db.insert("interface", "history", data)
        return data

    def execute(self, data):
        """
        :param data:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        self.replace_variable(data)
        self.make_request(data)
        self.convert_format(data)
        self.execute_assertion(data)
        self.extract_variables(data)
        self.record_result(data)
        print(g.data)
        return data
