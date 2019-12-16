
from flask import request
from flask.views import View


class CloverView(View):

    def dispatch_request(self):
        func = request.path.split('/')[-1]
        return getattr(self, func)()