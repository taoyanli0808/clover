
from clover.common.extractor import Extractor


class Validator():

    def __init__(self, data=None):
        self.data = data
        self.extractor = Extractor()

    def _assert(self): pass

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
