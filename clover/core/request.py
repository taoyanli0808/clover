
from requests import request
from requests.exceptions import InvalidURL
from requests.exceptions import MissingSchema
from requests.exceptions import InvalidSchema
from requests.exceptions import ConnectionError
from requests.exceptions import InvalidHeader

from clover.core.logger import Logger
from clover.core.response import Response
from clover.core.exception import ResponseException


class Request(object):

    def __init__(self, case):
        """
        :param case:
        """
        self.method = self.set_method(case.method)
        self.host, self.path, self.url = case.host, case.path, case.host + case.path
        self.header = self.set_header(case.header)
        self.body_mode, self.body = self.set_body(case.body)
        self.parameter = self.set_parameter(case.params)

    def set_method(self, method):
        """
        # 目前仅支持get、post、put与delete请求。
        :param method:
        :return:
        """
        return method.lower() if method.lower() in ['get', 'post', 'put', 'delete'] else 'get'

    def set_header(self, header):
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
        mode = body.get('mode', 'raw')
        if body:
            if mode in ['formdata', 'urlencoded']:
                body = {item['key']: item['value'] for item in body['data']}
            elif mode in ['file']:
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
        return mode, body

    def send_request(self):
        Logger.log("准备发送http请求，请求方法[{}]".format(self.method), "发送请求")
        Logger.log("准备发送http请求，请求域名[{}]".format(self.host), "发送请求")
        Logger.log("准备发送http请求，请求路径[{}]".format(self.path), "发送请求")
        Logger.log("准备发送http请求，请求地址[{}]".format(self.url), "发送请求")
        Logger.log("准备发送http请求，请求头[{}]".format(self.header), "发送请求")
        Logger.log("准备发送http请求，请求参数[{}]".format(self.parameter), "发送请求")
        Logger.log("准备发送http请求，请求体类型[{}]".format(self.body_mode), "发送请求")
        Logger.log("准备发送http请求，请求体[{}]".format(self.body), "发送请求")
        try:
            response = request(self.method, self.url, params=self.parameter, data=self.body, headers=self.header)
            Logger.log("发送http请求成功，响应码[{}]".format(response.status_code), "发送请求")
            Logger.log("发送http请求成功，请求耗时[{}]".format(response.elapsed), "发送请求")
            Logger.log("发送http请求成功，请求响应[{}]".format(response.text), "发送请求", 'debeg')
            return Response(response)
        except InvalidURL:
            self.status = 601
            self.message = "您输入接口信息有误，URL格式非法，请确认！"
            Logger.log("发送http请求出错，原因[{}]".format(self.message), "发送请求", 'warn')
            raise ResponseException()
        except MissingSchema:
            self.status = 602
            self.message = "您输入接口缺少协议格式，请增加[http(s)://]协议头！"
            Logger.log("发送http请求出错，原因[{}]".format(self.message), "发送请求", 'warn')
            raise ResponseException()
        except InvalidSchema:
            self.status = 603
            self.message = "不支持的接口协议，请使用[http(s)://]协议头！"
            Logger.log("发送http请求出错，原因[{}]".format(self.message), "发送请求", 'warn')
            raise ResponseException()
        except ConnectionError:
            self.status = 604
            self.message = "当链接到服务器时出错，请确认域名[{}]是否正确！".format(self.host)
            Logger.log("发送http请求出错，原因[{}]".format(self.message), "发送请求", 'warn')
            raise ResponseException()
        except InvalidHeader:
            self.status = 605
            self.message = "请求头包含非法字符！"
            Logger.log("发送http请求出错，原因[{}]".format(self.message), "发送请求", 'warn')
            raise ResponseException()
