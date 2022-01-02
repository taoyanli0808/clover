
from flask import request
from flask import jsonify

from clover.views import CloverView
from clover.keyword.service import KeywordService
from clover.core.exception import catch_exception


class KeywordView(CloverView):

    def __init__(self):
        super(KeywordView, self).__init__()
        self.service = KeywordService()

    @catch_exception
    def api_v1_keyword_create(self):
        """
        :return:
        """
        data = request.get_json()

        if 'keyword' not in data or not data['keyword']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'description' not in data or not data['description']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少功能描述!',
                'data': data
            })

        result = self.service.create(data)
        return jsonify({
            'status': 0,
            'message': "创建关键字成功！",
            'data': result
        })

    @catch_exception
    def api_v1_keyword_delete(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "删除关键字时缺少必要的ID",
                'data': data
            })

        id = self.service.delete(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': id
        })

    @catch_exception
    def api_v1_keyword_update(self):
        """
        :return:
        """
        data = request.get_json()

        if 'id' not in data or not data['id']:
            return jsonify({
                'status': 400,
                'message': "更新关键字时缺少必要的ID",
                'data': data
            })

        id = self.service.update(data)
        return jsonify({
            'status': 0,
            'message': '更新关键字成功！',
            'data': id
        })

    @catch_exception
    def api_v1_keyword_search(self):
        """
        :return:
        """
        data = request.get_json()

        total, result = self.service.search(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'total': total,
        })

    @catch_exception
    def api_v1_keyword_debug(self):
        """
        :return:
        """
        data = request.get_json()

        if 'keyword' not in data or not data['keyword']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少实现代码!',
                'data': data
            })

        if 'expression' not in data or not data['expression']:
            return jsonify({
                'status': 400,
                'message': '关键字缺少调用表达式!',
                'data': data
            })

        result = self.service.debug(data)
        return jsonify({
            'status': 0,
            'message': "关键字调试结束！",
            'data': result
        })
