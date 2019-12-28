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

    def create(self):
        """
        # 视图的创建操作。
        :return:
        """
        raise NotImplementedError

    def delete(self):
        """
        # 视图的删除操作。
        :return:
        """
        raise NotImplementedError

    def update(self):
        """
        # 视图的修改操作。
        :return:
        """
        raise NotImplementedError

    def search(self):
        """
        # 视图的查找操作。
        :return:
        """
        raise NotImplementedError

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
