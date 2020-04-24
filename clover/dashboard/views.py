
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.dashboard.service import DashboardService


class DashboardView(CloverView):

    def __init__(self):
        super(DashboardView, self).__init__()
        self.service = DashboardService()

    def search(self):
        pass
