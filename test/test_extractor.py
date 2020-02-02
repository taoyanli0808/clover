
import unittest

from clover.common.extractor import Extractor


class TestExpect(unittest.TestCase):

    def setUp(self):
        self.extractor = Extractor()

    def test_delimiter_bad_expression_type(self):
        result = self.extractor.extract_by_delimiter("", 3, "")
        self.assertIsNone(result)

    def test_delimiter_bad_data_string(self):
        result = self.extractor.extract_by_delimiter("123[]", "")
        self.assertIsNone(result)

    def test_delimiter_bad_data_string(self):
        data = '{"status": 0, "message": "ok", "data": [{"price": "13"}, {"price": "15"}]}'
        result = self.extractor.extract_by_delimiter(data, "status")
        self.assertEqual(0, result)
        result = self.extractor.extract_by_delimiter(data, "data.-1.price")
        self.assertEqual("15", result)


if __name__ == '__main__':
    unittest.main()
