import unittest

from clover.dashboard.service import DashboardService


class TestDashboard(unittest.TestCase):

    def setUp(self) -> None:
        self.obj = DashboardService()

    def test_get_info(self):
        print(self.obj.get_info())

    def tearDown(self) -> None:
        pass
