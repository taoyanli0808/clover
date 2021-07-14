"""
# Clover平台变量机制实现。
# author : taoyanli0808
# date   : 2020-05-27
# version: 1.2
# -------------------- Clover平台变量机制 --------------------
# clover平台变量分为4种类型，平台内置变量、自定义变量、触发变量与运行时变量
# 1、平台内置变量
# clover平台内置变量目前有response、request、keyword、variable、exception、
# validator、extractor共7个，详见各模块说明文档。
# 2、自定义变量
# 自定义变量（default）通过平台“配置管理-变量配置”页面进行添加，每个自定义
# 变量关联到团队与项目，同一团队下相同项目不能存在同名变量。自定义变量可以采用
# 字母、数字和下划线进行命名，但不可与平台内置变量重复。
# 3、触发变量
# 触发变量为通过页面或接口（包含Jenkins等插件）运行平台用例时用户提交的变量。
# 触发变量的优先级高于自定义变量，低于运行时变量。通常可以将域名设置为变量形
# 式，例如调试时使用自定义变量host指向测试环境http://test.52clover.cn，
# 当运行时采用触发变量重新指定host为http://www.52clover.cn覆盖自定义变量。
# 4、运行时变量
# 运行时变量通常为提取器提取的接口上下文变量，在用例执行生命周期内有效。
# 最常见的运行时变量使用场景为提取接口响应数据传递给下一个接口，使用提取器提取
# 接口响应数据保存为变量形式，下一个接口直接使用变量提取值。
# 5、变量优先级
# 平台内置变量 > 运行时变量 > 触发变量 > 自定义变量
"""

import re
from typing import Text

from clover.core import RESERVED
from clover.core.logger import Logger
from clover.core.request import Request
from clover.core.extractor import Extractor

from clover.models import query_to_dict
from clover.environment.models import VariableModel


class Variable(object):

    def __init__(self, case, trigger):
        """
        :param case:
        :param trigger:
        """
        self.team = case.team
        self.project = case.project
        self.extract = []
        if hasattr(trigger, 'variable'):
            self.trigger = trigger.variable
        else:
            self.trigger = []
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

    @staticmethod
    def is_reserved_variable(data):
        """
        # 内置变量使用时一般为：
        # ${response}.status
        # ${response}.header.contenttype
        # ${request}.path
        # 等，可见内置变量在被引用时在第一个位置
        :param data:
        :return:
        """
        # 这里如果data是空值则不处理。
        if not data or not isinstance(data, (Text,)):
            return False, None

        data = data.split('.')[0]

        match = re.search(r'\$\{(\w+?)\}', data)
        if match:
            variable = match.group(1).strip()
            if variable in RESERVED:
                return True, variable
        else:
            return False, None

    def derivation(self, data: Text):
        """
        :param data:
        :return:
        """
        # 这里如果data是空值则不处理。
        if not data or not isinstance(data, (Text,)):
            return data

        variables = re.findall(r'\$\{(\w+?)\}', data)
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

    def extract_variable_from_response(self, case, response):
        """
        :param case:
        :param response:
        :return:
        """
        Logger.log("提取接口间变量", "提取变量")
        # 这里是临时加的，这里要详细看下如何处理。
        if response is None or not hasattr(response, 'response'):
            Logger.log("响应为None或响应无数据。", "提取变量", level='warn')
            return

        if not hasattr(case, 'extract') or not case.extract:
            Logger.log("用例不需要提取变量。", "提取变量", level='warn')
            return case

        Logger.log("提取接口间变量开始[{}]".format(self.extract), "提取变量")
        for extract in case.extract:
            # 提取需要进行断言的数据
            selector = extract.get('selector', 'delimiter')
            extractor = Extractor(selector)
            expression = extract.get('expression', None)
            variable = extract.get('variable', None)

            # 表达式可能包含变量，使用值对变量进行替换。
            flag, reserved = self.is_reserved_variable(expression)
            if flag:
                if reserved == 'response':
                    index = expression.index('.')
                    _expression = expression[index + 1:]
                    if _expression == 'status':
                        result = response.status
                    elif _expression == 'elapsed':
                        result = response.elapsed
                    elif 'header' in _expression:
                        expr = _expression.split('.')[-1]
                        result = response.header.get(expr)
                    else:
                        result = extractor.extract(response.response, _expression, '.')
            else:
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
        Logger.log("提取接口间变量完成[{}]".format(self.extract), "提取变量")
