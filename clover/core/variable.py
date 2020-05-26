
import re
from typing import Text

from clover.core.request import Request
from clover.models import query_to_dict
from clover.environment.models import VariableModel

class Variable(object):

    def __init__(self, team, project, extract, trigger):
        self.team = team
        self.project = project
        self.extract = extract
        self.trigger = trigger
        self.variables = self.load_default_variable()

    def load_default_variable(self):
        """
        :return:
        """
        # 加载通过变量设置页面预置的变量数据。
        filter = {
            'team': self.team,
            'project': self.project
        }
        default = VariableModel.query.filter_by(**filter).all()

        return {
            'extract': self.extract,
            'trigger': self.trigger,
            'default': query_to_dict(default),
        }

    def derivation(self, data: Text):
        """
        :param data:
        :param variables:
        :return:
        """
        # 这里如果data是空值则不处理。
        if not data or not isinstance(Text):
            return data

        variables = re.findall(r'\$\{(.+?)\}', data)
        for variable in variables:
            if variable:
                variable = variable.strip()

                # 这里需要注意，变量的优先级是
                # 接口上下文变量 > 触发运行时指定变量 > 用户默认配置变量

                extract = self.variables['extract']
                for result in extract:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

                trigger = self.variables['trigger']
                for result in trigger:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

                default = self.variables['default']
                for result in default:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

        return data

    def replace_variable(self, request: Request) -> Request:
        request.url = self.derivation(request.url)
        if request.header:
            # self.logger.info("请求头替换前[{}]".format(case.get('header')))
            for header in request.header:
                header['value'] = self.derivation(header['value'])
            # self.logger.info("请求头换后[{}]".format(case.get('header')))
        if request.parameter:
            # self.logger.info("请求参数替换前[{}]".format(case.get('params')))
            for parameter in request.parameter:
                parameter['value'] = self.derivation(parameter['value'])
            # self.logger.info("请求参数换后[{}]".format(case.get('params')))

        if request.body:
            # self.logger.info("请求体替换前[{}]".format(case.get('body')))
            if request.body['mode'] in ['formdata', 'urlencoded']:
                for body in request.body:
                    body['value'] = self.derivation(body['value'])
            elif request.body['mode'] in ['file']:
                pass
            else:
                """
                # 这是"expected string or bytes-like object"问题的一个临时解决方案。
                # 原因是当body数据类型为raw，数据为json时，view层接收数据时自动将其转为
                # python对象，因此这里进行derivation会报错。
                """
                if isinstance(request.body['data'], (list,)):
                    for body in request.body['data']:
                        body['value'] = self.derivation(body['value'])
                else:
                    request.body['data'] = self.derivation(request.body['data'])
            # self.logger.info("请求体换后[{}]".format(case.get('body')))
        return request
