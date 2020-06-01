
from clover.core.response import Response
from clover.core.extractor import Extractor
from clover.core.logger import Logger, LogLevel


class Validator():

    def __init__(self, data=None):
        self.data = data
        self.extractor = Extractor()

    def _assert(self): pass

    def convert_type(self, convertor, data):
        """
        :param convertor:
        :param data:
        :return:
        """
        try:
            if convertor == 'int':
                return int(data)
            elif convertor == 'float':
                return float(data)
            elif convertor == 'boolean':
                return bool(data)
            else:
                return str(data)
        except ValueError:
            return data
        except TypeError:
            return data

    def verify(self, data, response: Response):
        # 这里载入验证项和验证过程是否需要分开？
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
                variable = extractor.extract(response.response, expression, '.')

                expected = verify.get('expected', None)
                # 转化预期结果为需要的数据类型，数据类型相同才能比较嘛
                convertor = verify.get('convertor', None)
                variable = self.convert_type(convertor, variable)
                # expected = self.convert_type(convertor, expected)

                # 获取比较器进行断言操作
                comparator = verify.get('comparator', None)

                result = self.compare(comparator, variable, expected)
                result = 'passed' if result else 'failed'
                # 如果有任何一个断言失败，接口的状态则改为失败。
                # if result == 'failed':
                #     self.result[data['name']]['status'] = 'failed'
                # # 保存断言信息。
                # self.result[data['name']]['result'].append({
                #     'status': result,
                #     'actual': variable,
                #     'expect': expected,
                #     'operate': comparator,
                # })
                Logger.log("断言，提取器[{}]".format(_extractor), "执行断言")
                Logger.log("断言，表达式[{}]".format(expression), "执行断言")
                Logger.log("断言，提取值[{}]".format(variable), "执行断言")
                Logger.log("断言，预期值[{}]".format(expected), "执行断言")
                Logger.log("断言，比较器[{}]".format(comparator), "执行断言")
                Logger.log("断言，变量值[{}]".format(result), "执行断言")
            except Exception as error:
                pass
                # # 断言异常时则认定为接口测试失败
                # self.result[data['name']]['status'] = 'failed'
                # # 保存断言异常信息
                # self.result[data['name']]['result'].append({
                #     'status': str(error)
                # })
                Logger.log("断言，执行异常[{}]".format(error), "执行断言", level=LogLevel.ERROR)

    def compare(self, comparator, variable, expected):
        """
        :param comparator:
        :param variable:
        :param expected:
        :return: 断言成功返回True，失败返回False，出错返回None
        """
        # 每个comparator对应一个validator的处理函数
        # 如果comparator不存在对应的处理函数则返回None
        func = getattr(self, comparator, None)
        if func is None or not callable(func):
            return None

        try:
            return func(variable, expected)
        except TypeError:
            return None

    def equal(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value == expected

    def not_equal(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value != expected

    def contain(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value in expected

    def not_contain(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value not in expected

    def greater(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value > expected

    def not_greater(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value <= expected

    def less(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value < expected

    def not_less(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return value >= expected
