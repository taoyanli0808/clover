"""
# description : base view for clover.
# author      : taoyanli0808
# history     :
#              2019/12/16 created
"""

from flask import request
from flask import jsonify
from flask.views import View


class CloverView(View):
    """
    # base view for clover.
    """

    def dispatch_request(self):
        """
        # split url and use last word as method name,
        # use getattr call method and return result.
        :return:
        """
        func = request.path.split('/')[-1]
        return getattr(self, func)()

    def response(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        if 'status' not in kwargs:
            kwargs.setdefault('status', 0)
        if 'message' not in kwargs:
            kwargs.setdefault('message', '')
        if 'data' not in kwargs:
            kwargs.setdefault('data', {})
        return jsonify(**kwargs)
