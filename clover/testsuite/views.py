
from flask import jsonify
from flask import request

from clover.views import CloverView
from clover.testsuite.service import Service


class TestSuiteView(CloverView):

    def __init__(self):
        super(TestSuiteView, self).__init__()

    def create(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def search(self):
        pass
