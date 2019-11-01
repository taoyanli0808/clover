#coding=utf-8

import time

import requests

from jsonpath import jsonpath

from common.utils.mongo import Mongo
from common.utils import get_timestamp
from common.utils import get_friendly_id
from common.utils.helper import derivation


class Service(object):

    def __init__(self):
        self.db = Mongo()

    def replace_variable(self, data):
        """
        # 这里对请求数据进行变量替换，将变量替换为具体值。
        # 变量和其值可以在"配置管理 -> 全局变量"里设置。
        # 目前支持host，header与param的变量替换。
        # 变量与值存储使用团队与项目进行区分，不同的团队与项目允许出现同名变量。
        :param data:
        :return:
        """
        filter = {
            'team': data.get('team'),
            'project': data.get('project')
        }
        results = self.db.search("environment", "variable", filter)

        data['host'] = derivation(data.get('host'), results)

        if 'header' in data:
            for key, value in data['header'].items():
                data['header'][key] = derivation(data['header'][key], results)

        if 'param' in data:
            for key, value in data['param'].items():
                data['param'][key] = derivation(data['param'][key], results)

        return data

    def execute(self, data):
        """
        :param data:
        :return: 返回值为元组，分别是flag，message和接口请求后的json数据。
        """
        data = self.replace_variable(data)

        # 发送http请求
        method = data.get("method")
        host = data.get("host")
        path = data.get("path")
        header = data.get('header', {})
        payload = data.get('param', {})
        url = host + path

        if method == 'get':
            response = requests.request(method, url, params=payload, headers=header)
        else:
            response = requests.request(method, url, data=payload, headers=header)
        # 解析请求结果
        result = response.json()
        # 执行断言
        flag = 0
        message = "测试成功"

        if response.status_code != 200:
            flag = 1
            message = "请求接口失败！"

        try:
            json = response.json()
        except Exception:
            flag = 3
            message = "响应数据非json"
            return flag, message, {}
        items = data.get('assert', [])
        for item in items:
            result = jsonpath(json, item['rule'])
            if not result:
                flag = 2
                message = "测试断言失败"
                break
            result = list(map(str, result))
            if result != [item['expect']]:
                flag = 2
                message = "测试断言失败"
                break

        return flag, message, json

    def save(self, data):
        """
        # 将页面数据保存到数据库。
        :param data:
        :return:
        """
        data['_id'] = get_friendly_id()
        self.db.insert("interface", "case", data)
        return data['_id']

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        # 需要通过case_id先查询到数据库里的测试用例。
        # run_id是一次运行的记录，查测试报告时使用。
        run_id = get_friendly_id()
        cases = []
        ids = data['cases']
        for id in ids.split(','):
            results = self.db.search('interface', 'case', {'_id': id})
            if not results:
                continue
            cases.append(results[0])

        # 这个data是要存储到数据库的测试报告数据。
        data = {
            'run_id': run_id,
            'time': {
                'start': 0,
                'end': 0,
                'cost': 0,
            },
            'count': {
                'total': 0,
                'run': 0,
                'success': 0,
                'fail': 0,
                'skip': 0
            },
            'result': []
        }
        start = time.time()
        # 判断每一个测试用例是否通过。
        for case in cases:
            case.setdefault('status', 0)
            case.setdefault('message', '测试通过！')
            data['count']['total'] += 1
            data['count']['run'] += 1
            status, message, _ = self.execute(case)
            if status == 0:
                data['count']['success'] += 1
            else:
                data['count']['fail'] += 1
                case['status'] = status
                case['message'] = message
            data['result'].append(case)
        print("{0} {1} {2} {3}".format(data['count']['total'], data['count']['run'], \
                                       data['count']['success'], data['count']['fail']))
        end = time.time()
        # 通过start与end时间戳计算整个测试耗时
        data['time']['start'] = get_timestamp(start)
        data['time']['end'] = get_timestamp(end)
        data['time']['cost'] = "共执行{0:0.3}秒".format(end - start)
        print(data)
        # 将测试报告数据写入数据库。
        self.db.insert('interface', 'report', data)
        print(run_id)
        return run_id

    def list(self, data):
        """
        :param data:
        :return:
        """
        results = self.db.search("interface", "case", data)
        return results if results else []

    def __del__(self):
        if self.db:
            self.db.close()
