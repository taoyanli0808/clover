import unittest

from worker import Worker


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.obj = Worker()

    def test_something(self):
        self.assertEqual(True, False)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
