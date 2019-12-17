"""
# description : base view for clover.
# author      : taoyanli0808
# history     :
#              2019/12/16 created
"""

from flask import request
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