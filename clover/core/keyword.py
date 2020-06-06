"""
# clover关键字机制预研第一版，主要实现执行关键字函数并返回结果。
# author ：taoyanli0808
# date   ：2020年6月6日22:03:10
# version：1.1.0
"""

import re

from clover.core.exception import KeywordException


class Keyword(object):

    def __init__(self, source):
        """
        :param source:
        """
        self.source = source
        self.function = None
        self.parameters = []
        self.function_name = None

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

        function = re.findall(r'\$\{(.+?)\(', keyword)
        if not function:
            print("不能提取关键字名称，执行失败！")
            return False
        self.function_name = function[0]

        parameters = re.findall(r'\$\{\w+\((.+?)\)\}', keyword)
        if not parameters:
            print("不能提取关键字参数，执行失败！")
            return False
        parameters = parameters[0]
        for param in parameters.split(','):
            self.parameters.append(param.strip())

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
                print("获取关键字失败！")
                raise KeywordException
            self.function = locals()[self.function_name]

            # 判断正则提取的参数与函数实际参数是否一致。
            parameter_count = locals()[self.function_name].__code__.co_argcount
            if len(self.parameters) != parameter_count:
                print("执行关键字时实际参数与所需参数不匹配")
                raise KeywordException

            # 从locals获取执行关键字所需参数列表。
            parameters = []
            for parameter in self.parameters:
                if parameter not in globals() and parameter not in locals():
                    print("找不到执行关键字的必要参数！")
                    continue
                if parameter in globals():
                    parameters.append(globals()[parameter])
                else:
                    parameters.append(locals()[parameter])
                    continue

            # 执行关键字并返回结果。
            return self.function(*parameters)
        except Exception as error:
            print("执行关键字时发生异常", error)


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
