
import json
import datetime

from flask import g
from requests import request
from requests.exceptions import InvalidURL
from requests.exceptions import MissingSchema
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError

from clover.common import derivation
from clover.common import convert_type
from clover.common.extractor import Extractor
from clover.common.validator import Validator

from clover.models import query_to_dict
from clover.environment.models import VariableModel


class Executor():

    def __init__(self, type='trigger'):
        g.data = []
        self.status = 0
        self.message = 'ok'
        self.type = type
        self.interface = 0
        self.verify = {
            'passed': 0,
            'failed': 0,
            'sikped': 0,
            'total': 0,
        }
        self.percent = 0.0
        self.start = 0
        self.end = 0
        self.result = {}    # 记录运行状态与相关数据。
        self.log = []       # log采用列表记录，保持运行时顺序。

    def replace_variable(self, case, data):
        """
        # 这里对请求数据进行变量替换，将变量替换为具体值。
        # 变量和其值可以在"配置管理 -> 全局变量"里设置。
        # 目前支持host，header与param的变量替换。
        # 变量与值存储使用团队与项目进行区分，不同的团队与项目允许出现同名变量。
        :param case:
        :param data:
        :return:
        """
        filter = {
            'team': case.get('team'),
            'project': case.get('project')
        }
        results = VariableModel.query.filter_by(**filter).all()

        variable = {
            'extract': g.data,
            'trigger': data.get('variables', []),
            'default': query_to_dict(results),
        }

        case['host'] = derivation(case.get('host'), variable)
        case['path'] = derivation(case.get('path'), variable)

        if 'header' in case:
            for header in case['header']:
                header['value'] = derivation(header['value'], variable)

        if 'params' in case:
            for param in case['params']:
                param['value'] = derivation(param['value'], variable)

        if 'body' in case:
            if case['body']['mode'] in ['formdata', 'urlencoded']:
                for param in case['body']['data']:
                    param['value'] = derivation(param['value'], variable)
            elif case['body']['mode'] in ['file']:
                pass
            else:
                case['body']['data'] = derivation(case['body']['data'], variable)

        self.log[-1].setdefault('variable', variable)

        return case

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
            header = {item['key']: item['value'].strip() for item in header if item['key']}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if params:
            params = {item['key']: item['value'] for item in params}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if body:
            if body['mode'] in ['formdata', 'urlencoded']:
                body = {item['key']: item['value'] for item in body['data']}
            elif body['mode'] in ['file']:
                pass
            else:
                body = body['data']

        try:
            response = request(
                method, url,
                params=params,
                data=body,
                headers=header
            )
            self.result[data['name']]['elapsed'] = response.elapsed.microseconds
        except InvalidURL:
            self.status = 601
            self.message = "您输入接口信息有误，URL格式非法，请确认！"
            return data
        except MissingSchema:
            self.status = 602
            self.message = "您输入接口缺少协议格式，请增加[http(s)://]协议头！"
            return data
        except InvalidSchema:
            self.status = 603
            self.message = "不支持的接口协议，请使用[http(s)://]协议头！"
            return data
        except ConnectionError:
            self.status = 604
            self.message = "当链接到服务器时出错，请确认域名[{}]是否正确！".format(data.get('host'))
            return data

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

        self.log[-1].update({
            'url': url,
            'method': method,
            'header': header,
            'params': params,
            'body': body,
            'response': data.get('response', {}),
        })

        return data

    def validate_request(self, data):
        """
        :param data:
        :return:
        """
        self.result[data['name']]['result'] = []
        validator = Validator()
        for verify in data['verify']:
            try:
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
                result = 'passed' if result else 'failed'
                self.result[data['name']]['result'].append({
                    'status': result,
                    'actual': variable,
                    'expect': expected,
                    'operate': comparator,
                })
                # 这里是计算断言通过，失败，跳过与整体数量。
                self.verify[result] += 1
                self.verify['total'] += 1
            except Exception:
                self.result[data['name']]['result'].append({
                    'status': 'error'
                })

    def extract_variable(self, data):
        """
        :param data:
        :return:
        """
        # 这里是临时加的，这里要详细看下如何处理。
        if 'response' not in data:
            return

        if 'extract' not in data or not data['extract']:
            return data

        for extract in data['extract']:
            # 提取需要进行断言的数据
            extractor = Extractor(extract.get('selector', 'delimiter'))
            expression = extract.get('expression', None)
            variable = extract.get('variable', None)
            result = extractor.extract(data['response']['content'], expression, '.')
            g.data.append({'name': variable, 'value': result})

        self.log[-1].setdefault('extract', data.get('extract'))

        return data

    def execute(self, cases, data=None):
        """
        :param cases:
        :param data:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        self.start = datetime.datetime.now()
        for case in cases:
            self.log.append({'name': case['name']})
            self.result.setdefault(case['name'], {})
            self.result[case['name']]['start'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.replace_variable(case, data)
            self.send_request(case)
            self.validate_request(case)
            self.extract_variable(case)

            self.result[case['name']]['end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end = datetime.datetime.now()

        self.interface = len(cases)
        if self.verify['total'] == 0:
            self.percent = 0.0
        else:
            self.percent = round(100 * self.verify['passed'] / self.verify['total'], 2)
