
from clover.common.utils.extract import Extract


class Expect(Extract):

    def __init__(self, data=None):
        # super(Extract, self).__init__(asrt)
        self.data = data

    def _assert(self): pass

    def test(self):
        """
        :param asrt:
        :return: 断言成功返回True，失败返回False，出错返回None
        """
        for asrt in self.data['verify']:
            extractor = asrt.get('extractor', 'delimiter')
            expression = asrt.get('expression')
            condition = asrt.get('condition', 'equal')
            expected = asrt.get('expected')

            # 每个condition对应一个expect的处理函数
            # 如果condition不存在对应的处理函数则返回None
            func = getattr(self, condition, None)
            if func is None or not callable(func):
                return None

            # 目前只支持正则和分隔符法提取数据进行断言。
            content = self.data['response']['content']
            if extractor == 're':
                value = self.extract_by_re(content, expression)
            elif extractor == 'delimiter':
                value = self.extract_by_delimiter(content, expression)
            else:
                return None

            status = func(value, expected)
            print(5*'-', value, expected, status)
            asrt.setdefault('result', {
                'status': status
            })

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
