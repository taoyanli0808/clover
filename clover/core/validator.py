
import config

from clover.core.logger import Logger
from clover.core.extractor import Extractor


class Validator():

    def __init__(self, data=None):
        self.data = data
        self.status = 'failed'
        self.result = []
        self.threshold = 1.0
        self.level = 0
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

    def performance(self, response):
        """
        # 这里对接口性能进行统计，先获取全局配置的性能门限值，默认全局配置为1000耗秒；
        # 注意需要转换全局门限值为秒，因为response.elapsed为秒。
        # 将响应中的时间数据与response.elapsed做比值，然后转化为百分比；
        # 如果level小于100%则说明符合预期，如果level大于100%则性能不达标。
        :param response:
        """
        if 'performance' in config.GLOBALS:
            try:
                self.threshold = float(config.GLOBALS.get('performance', 1000) / 1000)
            except ValueError:
                self.threshold = 1.0

        if response is not None:
            self.level = round(100 * response.elapsed / self.threshold, 2)
        else:
            self.level = 0.0

    def verify(self, case, response):
        """
        :param case:
        :param response:
        :return:
        """
        for verify in case.verify:
            _extractor, expression, variable, expected, comparator = None, None, None, None, None
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
                expected = self.convert_type(convertor, expected)

                # 获取比较器进行断言操作
                comparator = verify.get('comparator', None)

                result = self.compare(comparator, variable, expected)
                # 保存断言信息。
                self.result.append({
                    'status': result,
                    'actual': variable,
                    'expect': expected,
                    'operate': comparator,
                })
                Logger.log("断言，执行通过[{}]", "执行断言")
                Logger.log("断言，提取器[{}]".format(_extractor), "执行断言")
                Logger.log("断言，表达式[{}]".format(expression), "执行断言")
                Logger.log("断言，提取值[{}]".format(variable), "执行断言")
                Logger.log("断言，预期值[{}]".format(expected), "执行断言")
                Logger.log("断言，比较器[{}]".format(comparator), "执行断言")
                Logger.log("断言，变量值[{}]".format(result), "执行断言")
            except Exception as error:
                # 断言异常时则认定为接口测试失败
                self.result.append({
                    'status': 'error',
                    'actual': variable,
                    'expect': expected,
                    'operate': comparator,
                })
                Logger.log("断言，执行异常[{}]".format(error), "执行断言", level='error')
                Logger.log("断言，提取器[{}]".format(_extractor), "执行断言", level='error')
                Logger.log("断言，表达式[{}]".format(expression), "执行断言", level='error')
                Logger.log("断言，提取值[{}]".format(variable), "执行断言", level='error')
                Logger.log("断言，预期值[{}]".format(expected), "执行断言", level='error')
                Logger.log("断言，比较器[{}]".format(comparator), "执行断言", level='error')

        # 这里对断言结果进行统计，全部为passed才认为接口断言通过。
        status = [result['status'] for result in self.result]
        self.status = 'passed' if {True} == set(status) else 'failed'

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
