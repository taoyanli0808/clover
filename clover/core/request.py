
from typing import List
from typing import Dict
from typing import Text

from requests import request
from requests.exceptions import InvalidURL
from requests.exceptions import MissingSchema
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidHeader

from clover.core.response import Response
from clover.core.exception import ResponseException


class Request(object):

    def __init__(self, method: Text, host: Text, path: Text,
                 header: List, parameter: List, body: Dict) -> None:
        self.method = self.set_method(method)
        self.url = host.strip() + path.strip()
        self.header = self.set_header(header)
        self.body = self.set_body(body)
        self.parameter = self.set_parameter(parameter)

    def set_method(self, method):
        """
        # 目前仅支持get、post、put与delete请求。
        :param method:
        :return:
        """
        return method.lower() if method.lower() in ['get', 'post', 'put', 'delete'] else 'get'

    def set_header(self, header: List) -> Dict:
        """
        # 将数据库中取到的[{'a': 1}, {'b': 2}]转化为requests请求需要的{'a': 1, 'b': 2}
        # 注意，这里如果请求头包含前导空格会报InvalidHeader错误，所以建议对数据进行strip操作。
        :param header:
        :return:
        """
        return {item['key'].strip(): item['value'].strip() for item in header if item['key']} if header else {}

    def set_parameter(self, parameter):
        """
        # 将数据库中取到的[{'a': 1}, {'b': 2}]转化为requests请求需要的{'a': 1, 'b': 2}
        :param parameter:
        :return:
        """
        return {item['key']: item['value'] for item in parameter} if parameter else {}

    def set_body(self, body):
        """
        #
        :param body:
        :return:
        """
        if body:
            if body['mode'] in ['formdata', 'urlencoded']:
                body = {item['key']: item['value'] for item in body['data']}
            elif body['mode'] in ['file']:
                pass
            else:
                # 当请求时有中文出现会报UnicodeEncodeError，暂时强制转UTF-8
                """
                # 这里是"'list' object has no attribute 'encode'"问题的一个临时解决方案
                # 原因是当body数据类型为raw，数据为json时，view层接收数据时自动将其转为
                # python对象，如果对象不为字符串（通常不为），encode会报错。
                """
                if isinstance(body['data'], (str,)):
                    body = body['data'].encode('utf-8') if body['data'] else None
                else:
                    body = body['data']
        return body

    def send_request(self):
        try:
            response = request(self.method, self.url, params=self.parameter, data=self.body, headers=self.header)
            return Response(response)
            # self.result[data['name']]['elapsed'] = response.elapsed.microseconds
            # self.logger.error("接口请成功，耗时[{}]毫秒".format(response.elapsed.microseconds))
        except InvalidURL:
            self.status = 601
            self.message = "您输入接口信息有误，URL格式非法，请确认！"
            # self.result[data['name']]['status'] = 'error'
            self.logger.error("接口请失败，[{}]".format(self.message))
            raise ResponseException()
        except MissingSchema:
            self.status = 602
            self.message = "您输入接口缺少协议格式，请增加[http(s)://]协议头！"
            # self.result[data['name']]['status'] = 'error'
            self.logger.error("接口请失败，[{}]".format(self.message))
            return ResponseException()
        except InvalidSchema:
            self.status = 603
            self.message = "不支持的接口协议，请使用[http(s)://]协议头！"
            # self.result[data['name']]['status'] = 'error'
            self.logger.error("接口请失败，[{}]".format(self.message))
            return ResponseException()
        except ConnectionError:
            self.status = 604
            self.message = "当链接到服务器时出错，请确认域名[{}]是否正确！".format(data.get('host'))
            # self.result[data['name']]['status'] = 'error'
            self.logger.error("接口请失败，[{}]".format(self.message))
            return ResponseException()
        except InvalidHeader:
            self.status = 605
            self.message = "请求头包含非法字符！"
            # self.result[data['name']]['status'] = 'error'
            self.logger.error("接口请失败，[{}]".format(self.message))
            return ResponseException()
