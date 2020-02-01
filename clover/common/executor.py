
import json
import datetime

from flask import g
from requests import request
from requests.exceptions import InvalidURL
from requests.exceptions import MissingSchema
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from sqlalchemy.exc import ProgrammingError

from clover.exts import db
from clover.models import query_to_dict
from clover.common import derivation
from clover.common import convert_type
from clover.common import get_mysql_error
from clover.common import get_system_info
from clover.common.extractor import Extractor
from clover.common.validator import Validator
from clover.report.models import ReportModel
from clover.environment.models import VariableModel


class Executor():

    def __init__(self, type='trigger'):
        g.data = []
        self.status = 0
        self.message = 'ok'
        self.type = type
        self.result = {}

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

        keyword = {
            'extract': g.data,
            'trigger': data.get('variables', []),
            'default': query_to_dict(results),
        }

        case['host'] = derivation(case.get('host'), keyword)
        case['path'] = derivation(case.get('path'), keyword)

        if 'header' in case:
            for header in case['header']:
                header['value'] = derivation(header['value'], keyword)

        if 'params' in case:
            for param in case['params']:
                param['value'] = derivation(param['value'], keyword)

        if 'body' in case:
            for param in case['body']:
                param['value'] = derivation(param['value'], keyword)

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
            header = {item['key']: item['value'] for item in header if item['key']}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if params:
            params = {item['key']: item['value'] for item in params}

        # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
        if body:
            body = {item['key']: item['value'] for item in body}

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
            except Exception:
                self.result[data['name']]['result'].append({
                    'status': 'error'
                })

    def extract_variables(self, data):
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

    def execute(self, cases, data=None):
        """
        :param cases:
        :param data:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        start = datetime.datetime.now()
        for case in cases:
            self.result.setdefault(case['name'], {})
            self.result[case['name']]['start'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.replace_variable(case, data)
            self.send_request(case)
            self.validate_request(case)
            self.extract_variables(case)
            self.record_result(case)
            self.result[case['name']]['end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.now()

        # 调试模式不生成测试报告！
        if self.type == 'debug':
            return cases

        # 这里是一个适配操作，如果report字段存在则用于报告的name属性，
        # 否则这里取套件或者是接口的name属性给report的name属性，相当
        # 与可以让用户传递最终测试报告的报告名，仅此而已。
        # https://github.com/taoyanli0808/clover/issues/39
        name = data['report'] if 'report' in data and data['report'] else data['name']
        report = {
            'team': data['team'],
            'project': data['project'],
            'name': name,
            'type': 'interface',
            'start': start,
            'end': end,
            'duration': (end - start).total_seconds(),
            'platform': get_system_info(),
            'detail': self.result,
        }

        model = ReportModel(**report)
        db.session.add(model)
        # 这是一个处理数据库异常的例子，后面最好有统一的处理方案。
        try:
            db.session.commit()
        except ProgrammingError as error:
            code, msg = get_mysql_error(error)
            return (code, msg)
        return model.id
