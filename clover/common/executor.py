
import json

import requests

from flask import g

from clover.common import derivation
from clover.common import convert_type
from clover.common.extractor import Extractor
from clover.common.validator import Validator
from clover.environment.models import VariableModel


class Executor():

    def __init__(self, type='trigger'):
        g.data = []
        self.type = type
        self.report = {}

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
                header['value'] = derivation(header['value'], results)

        if 'params' in data:
            for param in data['params']:
                param['value'] = derivation(param['value'], results)

        if 'body' in data:
            for param in data['body']:
                param['value'] = derivation(param['value'], results)

        return data

    def send_request(self, data):
        """
        :param data:
        :return:
        """
        # 发送http请求
        method = data.get("method")
        host = data.get("host")
        path = data.get("path")
        header = data.get('header', {})
        params = data.get('params', {})
        body = data.get('body', {})
        url = host + path

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if header:
            header = {item['key']: item['value'] for item in header if item['key']}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if params:
            params = {item['key']: item['value'] for item in params}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if body:
            body = {item['key']: item['value'] for item in body}

        response = requests.request(
            method, url,
            params=params,
            data=body,
            headers=header
        )

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
            data['response']['json'] = {"message": "亲爱的小伙伴，目前接口仅支持json格式！"}

        return data

    def validate_request(self, data):
        """
        :param data:
        :return:
        """
        validator = Validator()
        for verify in data['verify']:
            # 判断提取器是否合法，只支持三种提取器
            _extractor = verify.get('extractor', 'delimiter')
            if _extractor not in ['delimiter', 'regular', 'keyword']:
                # 这里最好给一个报错
                continue
            # 提取需要进行断言的数据
            extractor = Extractor(_extractor)
            expression = verify.get('expression', None)
            variable = extractor.extract(data['response']['content'], expression, '.')

            expected = verify.get('expected', None)
            # 转化预期结果为需要的数据类型，数据类型相同才能比较嘛
            convertor = verify.get('convertor', None)
            variable = convert_type(convertor, variable)
            expected = convert_type(convertor, expected)

            # 获取比较器进行断言操作
            comparator = verify.get('comparator', None)

            result = validator.compare(comparator, variable, expected)

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

    def execute(self, cases):
        """
        :param cases:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        for case in cases:
            self.replace_variable(case)
            self.send_request(case)
            self.validate_request(case)
            self.extract_variables(case)
            self.record_result(case)
        if self.type == 'debug':
            return cases
        else:
            return self.report
