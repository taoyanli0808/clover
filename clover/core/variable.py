
import re
from typing import Text

from clover.core.logger import Logger
from clover.core.request import Request
from clover.core.response import Response
from clover.core.extractor import Extractor

from clover.models import query_to_dict
from clover.environment.models import VariableModel

class Variable(object):

    def __init__(self, team, project, trigger):
        """
        :param team:
        :param project:
        :param trigger:
        """
        self.team = team
        self.project = project
        self.extract = []
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
        return query_to_dict(default)

    def derivation(self, data: Text):
        """
        :param data:
        :param variables:
        :return:
        """
        # 这里如果data是空值则不处理。
        if not data or not isinstance(data, (Text,)):
            return data

        variables = re.findall(r'\$\{(.+?)\}', data)
        for variable in variables:
            if variable:
                variable = variable.strip()

                # 这里需要注意，变量的优先级是
                # 接口上下文变量 > 触发运行时指定变量 > 用户默认配置变量

                extract = self.extract
                for result in extract:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

                trigger = self.trigger
                for result in trigger:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

                print(self.variables)
                default = self.variables
                for result in default:
                    if variable == result['name']:
                        data = data.replace('${' + variable + '}', str(result['value']))

        return data

    def replace_variable(self, request: Request) -> Request:
        request.url = self.derivation(request.url)
        if request.header:
            Logger.log("请求头替换前[{}]".format(request.header), "变量替换")
            for key, value in request.header.items():
                request.header[key] = self.derivation(value)
            Logger.log("请求头替换后[{}]".format(request.header), "变量替换")
        if request.parameter:
            Logger.log("请求参数替换前[{}]".format(request.parameter), "变量替换")
            for key, value in request.parameter.items():
                request.parameter[key] = self.derivation(value)
            Logger.log("请求参数替换后[{}]".format(request.parameter), "变量替换")

        if request.body:
            Logger.log("请求体替换前[{}]".format(request.body), "变量替换")
            if request.body_mode in ['formdata', 'urlencoded']:
                for key, value in request.body.items():
                    request.body[key] = self.derivation(value)
            elif request.body_mode in ['file']:
                pass
            else:
                """
                # 这是"expected string or bytes-like object"问题的一个临时解决方案。
                # 原因是当body数据类型为raw，数据为json时，view层接收数据时自动将其转为
                # python对象，因此这里进行derivation会报错。
                """
                if isinstance(request.body, (list,)):
                    for key, value in request.body.items():
                        request.body[key] = self.derivation(value)
                else:
                    request.body = self.derivation(request.body)
            Logger.log("请求体替换前[{}]".format(request.body), "变量替换")
        return request

    def extract_variable_from_response(self, data, response: Response):
        Logger.log("提取接口间变量", "变量替换")
        # 这里是临时加的，这里要详细看下如何处理。
        if 'response' not in response.response:
            return

        if 'extract' not in data or not data['extract']:
            return data

        Logger.log("提取接口间变量开始[{}]".format(self.extract), "变量替换")
        for extract in data['extract']:
            # 提取需要进行断言的数据
            selector = extract.get('selector', 'delimiter')
            extractor = Extractor(selector)
            expression = extract.get('expression', None)
            variable = extract.get('variable', None)
            result = extractor.extract(response.response, expression, '.')
            """
            # 这里不要简单的append，如果两个变量name相同，value不一样，
            # 后面被追加进来的数据不会生效，因此变量在这里要保证唯一性。
            """
            for _varibale in self.extract:
                if variable == _varibale['name']:
                    _varibale['value'] = result
                    break
            else:
                self.extract.append({'name': variable, 'value': result})
        Logger.log("提取接口间变量完成[{}]".format(self.extract), "变量替换")
