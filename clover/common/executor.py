"""
Chapter 1
The cases may be an interface or a suite.The suite is a collection of multiple interfaces.
Host, path, header, parameter and body support parameterized variables, you can use ${var}
to represent the value of the variable var.The parameters passed between interfaces extracted
by extract are also considered as variables, and the value of extract['varibale'] is the variable name.
    cases: [
        {
            'id': 25,
            'team': 'qa',
            'project': 'testing platform',
            'name': 'alibaba map',
            'method': 'get',
            'host': '${ditu}',
            'path': '/service/regeo',
            'header': [
                {
                    'key': 'clover',
                    'value': '0.3.4'
                }
            ],
            'params': [
                {
                    'key': 'longitude',
                    'value': '121.04925573429551'
                },
                {
                    'key': 'latitude',
                    'value': '31.315590522490712'
                }
            ],
            'body': {
                'data': '',
                'mode': 'raw'
            },
            'verify': [
                {
                    'expected': '1',
                    'convertor': 'int',
                    'extractor': 'delimiter',
                    'comparator': 'equal',
                    'expression': 'status'
                },
                {
                    'expected': '苏州市',
                    'convertor': 'str',
                    'extractor': 'delimiter',
                    'comparator': 'equal',
                    'expression': 'data.city'
                },
                {
                    'expected': '512',
                    'convertor': 'int',
                    'extractor': 'regular',
                    'comparator': 'equal',
                    'expression': '\\"areacode\\":\\"(.+?)\\",'
                }
            ],
            'extract': [
                {
                    'selector': 'delimiter',
                    'variable': 'data',
                    'varibale': '',
                    'expression': 'status'
                }
            ],
            'enable': 0,
            'created': '2020-02-07T13:52:23',
            'updated': '2020-04-19T14:15:19'
        },
        ...
    ]
------------------------------------------- It's a gorgeous divider -------------------------------------------
Chapter 2
Executor uses the result property to record the result of execution.
The structure of the result property is used for data presentation of the report detail page, as follows:
    result: {
        'name1': {
            'status': 'passed',                     # ['passed', 'failed', 'error', 'skiped']
            'start': '2020-04-24 14:59:56',
            'end': '2020-04-24 14:59:57',
            'elapsed': 238568,
            'result': [
                {
                    "actual": 1,
                    "expect": 1,
                    "status": "passed",
                    "operate": "equal"
                }, {
                    "actual": "苏州市",
                    "expect": "苏州市",
                    "status": "passed",
                    "operate": "equal"
                }, {
                    "actual": 512,
                    "expect": 512,
                    "status": "passed",
                    "operate": "equal"
                }
            ]
        },
        'name2': {}
    }
"""

import os
import logging
import datetime

from clover.core.request import Request
from clover.core.variable import Variable
from clover.core.extractor import Extractor
from clover.core.validator import Validator

from clover.dashboard.service import DashboardService


class Executor():

    def __init__(self, type='trigger', log='default'):
        self.variables = []
        self.status = 0
        self.message = 'ok'
        self.type = type
        self.start = 0
        self.end = 0
        self.result = {}    # 记录运行状态与相关数据。
        self.interface = {
            'verify': 0,
            'passed': 0,
            'failed': 0,
            'error': 0,
            'sikped': 0,
            'total': 0,
            'percent': 0.0,
        }

        file = os.path.join(os.getcwd(), 'logs', '{}.log'.format(log))
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(file)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
        self.logger.info("[{}]接口测试第1步，变量替换".format(case['name']))
        self.logger.info("查找预定义变量，查找条件[{}]".format(filter))
        self.logger.info("变量查找成功，预定义变量{}".format(variable['default']))
        self.logger.info("变量查找成功，触发时变量{}".format(variable['trigger']))
        self.logger.info("变量查找成功，运行时变量{}".format(variable['extract']))
        self.logger.info("域名替换前[{}]".format(case.get('host')))
        self.logger.info("域名替换后[{}]".format(case.get('host')))
        self.logger.info("路径替换前[{}]".format(case.get('path')))
        self.logger.info("路径替换后[{}]".format(case.get('path')))

        return case

    def send_request(self, data):
        """
        :param data:
        :return:
        """
        self.logger.info("[{}]接口测试第2步，发送接口请求".format(data['name']))
        team = data.get("team")
        project = data.get("project")
        trigger = data.get("trigger")
        # 发送http请求
        method = data.get("method")
        host = data.get("host")
        path = data.get("path")
        header = data.get('header', {})
        params = data.get('params', {})
        body = data.get('body', {})

        self.logger.info("接口请求方法[{}]".format(method))
        self.logger.info("接口请求域名[{}]".format(host))
        self.logger.info("接口请求路径[{}]".format(path))
        self.logger.info("接口请求头[{}]".format(header))
        self.logger.info("接口请求参数[{}]".format(params))
        self.logger.info("接口请求体[{}]".format(body))

        variable = Variable(team, project, trigger, extract)
        request = Request(method, host, path, header, params, body)
        validator = Validator()

        variable.replace_variable(request)
        response = request.send_request()

        self.logger.info("接口请成功，响应状态码[{}]".format(response.status))
        self.logger.info("接口请成功，响应头信息[{}]".format(response.header))
        self.logger.info("接口请成功，响应内容为[{}]".format(response.response))

        return response

    def validate_request(self, data):
        """
        :param data:
        :return:
        """
        self.logger.info("[{}]接口测试第3步，接口结果断言".format(data['name']))
        self.result[data['name']]['result'] = []

    def extract_variable(self, data):
        """
        :param data:
        :return:
        """
        self.logger.info("[{}]接口测试第4步，提取接口间变量".format(data['name']))
        # 这里是临时加的，这里要详细看下如何处理。
        if 'response' not in data:
            return

        if 'extract' not in data or not data['extract']:
            return data

        for extract in data['extract']:
            # 提取需要进行断言的数据
            selector = extract.get('selector', 'delimiter')
            extractor = Extractor(selector)
            expression = extract.get('expression', None)
            variable = extract.get('variable', None)
            result = extractor.extract(data['response']['content'], expression, '.')
            """
            # 这里不要简单的append，如果两个变量name相同，value不一样，
            # 后面被追加进来的数据不会生效，因此变量在这里要保证唯一性。
            """
            for _varibale in self.variables:
                if variable == _varibale['name']:
                    _varibale['value'] = result
                    break
            else:
                self.variables.append({'name': variable, 'value': result})

            self.logger.info("提取，选择器[{}]".format(selector))
            self.logger.info("断言，表达式[{}]".format(expression))
            self.logger.info("断言，变量名[{}]".format(variable))
            self.logger.info("断言，变量值[{}]".format(result))

        return data

    def sync_dashboard(self, data):
        """
        # Use suite, name and identifier to uniquely mark a record.
        # If the record does not exist, it will be created. Otherwise, it will be updated.
        :param data:
        :return:
        """
        service = DashboardService()
        filter = {
            'team': data.get('team'),
            'project': data.get('project'),
            'suite': 0,
            'name': data.get('name'),
            'identifier': data.get('id'),
        }
        _, history = service.search(filter)

        if history:
            history = history[0]
            # get status from result property then update history
            status = self.result[data['name']]['status']
            history['statistics'][status] += 1
            history['statistics']['percent'] = round(
                100 * history['statistics']['passed'] / history['statistics']['total'], 2)
            service.update(history)
        else:
            history = {
                'team': data.get('team'),
                'project': data.get('project'),
                'type': 'interface',
                'suite': 0,
                'name': data.get('name'),
                'identifier': data.get('id'),
                'statistics': {
                    'passed': 0,
                    'failed': 0,
                    'error': 0,
                    'skiped': 0,
                    'total': 0,
                    'percent': 0,
                },
                'score': 0,  # 这里需要写函数实现
            }

            # get status from result property then create history
            status = self.result[data['name']]['status']
            history['statistics'][status] += 1
            history['statistics']['percent'] = round(
                100 * history['statistics']['passed'] / history['statistics']['total'], 2)
            service.create(history)

    def statistics(self):
        """
        # Statistics interface success, failure, error, skip and success rate.
        :return:
        """
        for _, results in self.result.items():
            self.interface['verify'] += len(results['result'])
            if results['status'] == 'passed':
                self.interface['passed'] += 1
            if results['status'] == 'failed':
                self.interface['failed'] += 1
            if results['status'] == 'error':
                self.interface['error'] += 1
            if results['status'] == 'skiped':
                self.interface['skiped'] += 1
        if self.interface['total'] == 0:
            self.interface['percent'] = 0.0
        else:
            self.interface['percent'] = round(100 * self.interface['passed'] / self.interface['total'], 2)

    def execute(self, cases, data=None):
        """
        :param cases:
        :param data:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        self.start = datetime.datetime.now()
        for case in cases:
            self.logger.info("[{}]接口测试开始...".format(case['name']))
            self.result.setdefault(case['name'], {'status': 'passed'})
            self.result[case['name']]['start'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            self.replace_variable(case, data)
            self.send_request(case)
            self.validate_request(case)
            self.extract_variable(case)
            # self.sync_dashboard(case)

            self.result[case['name']]['end'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info("[{}]接口测试结束...".format(case['name']))
        self.end = datetime.datetime.now()

        # self.statistics()
        self.logger.info("接口[{}],断言个数[{}],成功率[{}]".format(self.interface['total'], self.interface['verify'], self.interface['percent']))
