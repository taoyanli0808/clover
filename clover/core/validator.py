from clover import config

from clover.core.extractor import Extractor


class Validator():

    def __init__(self, data=None):
        self.data = data
        self.status = 'failed'
        self.result = []
        self.threshold = 1.0
        self.level = 'failed'
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
            # self.level = round(100 * response.elapsed / self.threshold, 2)
            self.level = 'passed' if response.elapsed < self.threshold else 'failed'

    @staticmethod
    def set_default_verify(case):
        """
        :param case:
        :return:
        """
        # 这里先对用例的所有提取表达式进行检索，看是否存在状态码验证，不存在则添加。
        expressions = [verify.get('expression') for verify in case.verify]
        if '${response}.status' not in expressions:
            case.verify.append({
                'expected': 200,
                'convertor': "int",
                'extractor': "delimiter",
                'comparator': "equal",
                'expression': "${response}.status"
            })

    def verify(self, case, response, variable, report):
        """
        :param case:
        :param response:
        :param variable:
        :param report:
        :return:
        """
        if not case.status:
            self.status = 'skiped'
            # 接口跳过运行时统计skiped加1
            report.report['interface']['skiped'] += 1
            return

        if self.status == 'error':
            # 接口请求时若发生错误error加1
            report.report['interface']['error'] += 1
            return

        self.set_default_verify(case)
        for verify in case.verify:
            _extractor, _expression, _variable, _expected, comparator = None, None, None, None, None
            try:
                # 判断提取器是否合法，只支持三种提取器
                _extractor = verify.get('extractor', 'delimiter')
                if _extractor not in Extractor.VALID_TYPE:
                    # 这里最好给一个报错
                    continue
                # 提取需要进行断言的数据
                extractor = Extractor(_extractor)

                expression = verify.get('expression', None)
                # 表达式可能包含变量，使用值对变量进行替换。
                flag, reserved = variable.is_reserved_variable(expression)
                if flag:
                    if reserved == 'response':
                        index = expression.index('.')
                        _expression = expression[index+1:]
                        if _expression == 'status':
                            _variable = response.status
                        elif _expression == 'elapsed':
                            _variable = response.elapsed
                        elif 'header' in _expression:
                            expr = _expression.split('.')[-1]
                            _variable = response.header.get(expr)
                        else:
                            _variable = extractor.extract(response.response, _expression, '.')
                else:
                    _expression = variable.derivation(expression)
                    _variable = extractor.extract(response.response, _expression, '.')

                expected = verify.get('expected', None)
                # 预期结果可能包含变量，使用值对变量进行替换。
                _expected = variable.derivation(expected)

                # 转化预期结果为需要的数据类型，数据类型相同才能比较嘛
                convertor = verify.get('convertor', None)
                _variable = self.convert_type(convertor, _variable)
                _expected = self.convert_type(convertor, _expected)

                # 获取比较器进行断言操作
                comparator = verify.get('comparator', None)

                result = self.compare(comparator, _variable, _expected)
                # 保存断言信息。
                self.result.append({
                    'status': result,
                    'actual': _variable,
                    'expect': _expected,
                    'comparator': comparator,
                    'expression': _expression,
                    'extractor': _extractor,
                })
            except Exception as error:
                # 断言异常时则认定为接口测试失败
                self.result.append({
                    'status': 'error',
                    'actual': _variable,
                    'expect': _expected,
                    'operate': comparator,
                    'expression': _expression,
                    'extractor': _extractor,
                })

        # 这里对断言结果进行统计，全部为passed才认为接口断言通过。
        status = [result['status'] for result in self.result]
        self.status = 'passed' if {True} == set(status) else 'failed'

        if self.status == 'passed':
            report.report['interface']['passed'] += 1
        elif self.status == 'failed':
            report.report['interface']['failed'] += 1
        elif self.status == 'error':
            report.report['interface']['error'] += 1
        else:
            pass

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
        return expected in value

    def not_contain(self, value, expected):
        """
        :param value:
        :param expected:
        :return:
        """
        return expected not in value

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
