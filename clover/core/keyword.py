"""
# clover关键字机制预研第一版，主要实现执行关键字函数并返回结果。
# author ：taoyanli0808
# date   ：2020年6月6日22:03:10
# version：1.1.0
"""

import re

from clover.models import query_to_dict
from clover.keyword.models import KeywordModel

from clover.core.logger import Logger


class Keyword(object):

    def __init__(self, source):
        """
        :param source:
        """
        self.source = source
        self.function = None
        self.parameters = []
        self.function_name = None

    def _load_keywords(self, classify):
        """
        :param classify:
        :return:
        """
        filter = {'enable': 0, 'classify': classify}
        keywords = KeywordModel.query.filter_by(**filter).all()
        return query_to_dict(keywords)

    def _guess_parameter_type(self, data):
        """
        :param data:
        :return:
        """
        if not isinstance(data, (str,)):
            return data

        pattern = re.compile('\d+')
        if re.match(pattern, data):
            return int(data)

        pattern = re.compile('\d+\.\d+')
        if re.match(pattern, data):
            return float(data)

        # 这里增加下列表类型
        # 这里增加下字典类型
        # 这里增加下集合类型
        # 这里增加下元祖类型

    def get_function_name_from_source(self):
        """
        :return:
        """
        function = re.findall(r'def\s+(.+?)\(', self.source)
        if not function:
            Logger.log("不能提取关键字名称，执行失败！", "获取关键字名")
            return False
        return function[0]

    def is_keyword(self, keyword):
        """
        # 给定字符串keyword，判断次字符串是否为需要处理的关键字定义。
        # 例如接口验签需要动态计算，此时我们需要关键字机制支持，通常
        # 需要在页面声明这里是关键字${sign(secret, data)}。
        # 本函数判断字符串是否为关键字，既是否满足如上格式声明。
        :param keyword: ${function_name(*args, **kwargs)}
        :return: True如果通过keyword判定此处代码为关键字，否则返回False。
        """
        if not isinstance(keyword, (str,)):
            return False

        function = re.findall(r'\$\{(\w+?)\(', keyword)
        if not function:
            Logger.log("不能提取关键字名称，执行失败！", "关键字判定")
            return False
        self.function_name = function[0]

        parameters = re.findall(r'\$\{\w+\((.+?)\)\}', keyword)
        if not parameters:
            Logger.log("不能提取关键字参数，执行失败！", "关键字判定")
            return False
        parameters = parameters[0]
        for param in parameters.split(','):
            param = self._guess_parameter_type(param.strip())
            self.parameters.append(param)

        return self.function_name is not None and self.parameters

    def execute(self):
        """
        # 执行关键字需要先执行exec函数将关键字放入locals。
        # 获取参数需要进一步优化，目前参数在所有函数外因此
        # 从globals获取。
        :return:
        """
        try:
            exec(self.source)

            # 从locals获取执行关键字。
            if self.function_name not in locals():
                Logger.log("获取关键字失败！", "关键字执行")
                return
            self.function = locals()[self.function_name]

            # 判断正则提取的参数与函数实际参数是否一致。
            parameter_count = locals()[self.function_name].__code__.co_argcount
            if len(self.parameters) != parameter_count:
                Logger.log("执行关键字时实际参数与所需参数不匹配！", "关键字执行")
                return

            # 从locals获取执行关键字所需参数列表。
            # parameters = []
            # for parameter in self.parameters:
            #     print(self.parameters)
            #     print(locals())
            #     if parameter not in globals() and parameter not in locals():
            #         print("找不到执行关键字的必要参数！")
            #         Logger.log("找不到执行关键字的必要参数！", "关键字执行")
            #         continue
            #     if parameter in globals():
            #         parameters.append(globals()[parameter])
            #     else:
            #         parameters.append(locals()[parameter])
            #         continue
            exec(self.source)
            # 执行关键字并返回结果。
            result = None
            try:
                result = self.function(*self.parameters)
            except Exception as error:
                print(error)
            return result
        except Exception as error:
            Logger.log("执行关键字时发生异常{}".format(error), "关键字执行", level="error")

    def derivation(self, data):
        """
        :param data:
        :return:
        """
        # 这里如果data是空值则不处理。
        if not data or not isinstance(data, (str, bytes, )):
            return data

        if isinstance(data, (bytes, )):
            data = str(data, encoding="utf-8")

        flag = self.is_keyword(data)
        if not flag:
            return data
        Logger.log("发现关键字[{}]！".format(self.function_name), "关键字执行")

        # 查找关键字并执行
        for keyword in self.keywords:
            if keyword['name'] == self.function_name:
                Logger.log("关键字[{}]存在！".format(self.function_name), "关键字执行")
                self.source = keyword['keyword']
                return self.execute()
            return data

        return data

    def call_keyword(self, request, classify=None):
        """
        :param request:
        :return:
        """
        self.keywords = self._load_keywords(classify)

        if request.header:
            for key, value in request.header.items():
                request.header[key] = self.derivation(value)

        if request.parameter:
            for key, value in request.parameter.items():
                request.parameter[key] = self.derivation(value)

        if request.body:
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
                    value = self.derivation(request.body)
                    print("关键字执行结果：", value)
                    # request.body =
        return request


if __name__ == '__main__':
    secret = '123456'
    # data = 'abcdefg'
    source = """data = 'abcdefg'
def sign(secret, data):
    import hashlib
    raw = (secret + data).encode('utf-8')
    md5 = hashlib.md5()
    md5.update(raw)
    return md5.hexdigest()"""
    keyword = Keyword(source)
    keyword.is_keyword('${sign(secret, data)}')
    result = keyword.execute()
    print(result)
