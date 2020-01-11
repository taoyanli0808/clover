
import re
import os
import json
import unittest

import requests

from .expect import Expect
from clover.common.utils.HTMLTestRunner import HTMLTestRunner


def derivation(data, results):
    """
    :param data:
    :param results:
    :return:
    """
    # 这里如果data是空值或者变量没有设置则不处理。
    if not data or not results:
        return data

    variable = re.findall(r'\{(.+?)\}', data)
    if variable:
        print(variable)
        variable = variable[0].strip()
        for result in results:
            if variable == result.name:
                return result.value
    else:
        return data


def send_request(data):
    """
    :param data:
    :return:
    """
    # 发送http请求
    method = data.get("method")
    host = data.get("host")
    path = data.get("path")
    header = data.get('header', {})
    payload = data.get('params', {})
    url = host + path

    # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
    if header:
        header = {item['key']: item['value'] for item in header if item['key']}

    # 将[{'a': 1}, {'b': 2}]转化为{'a': 1, 'b': 2}
    if payload:
        payload = {item['key']: item['value'] for item in payload}

    if method == 'get':
        response = requests.request(method, url, params=payload, headers=header)
    else:
        response = requests.request(method, url, data=payload, headers=header)

    # 这里将响应的状态码，头信息和响应体单独存储，后面断言或提取变量会用到
    data['response'] = {
        'status': response.status_code,
        'header': dict(response.headers),
        'content': response.text
    }

    # 框架目前只支持json数据，在这里尝试进行json数据转换
    try:
        data['response']['json'] = json.loads(data['response']['content'])
    except Exception:
        data['response']['json'] = {}

    return data


def _make_test(data):
    """
    :param data:
    :return:
    """
    @staticmethod
    def test_abc(**kwargs):
        send_request(data)
        expect = Expect(data)
        expect.test()
    return test_abc


def run_case_use_unittest(cases):
    """
    :param data:
    :return:
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for i, case in enumerate(cases):
        # 使用type函数创建TestCase的子类，使用反射方法创建测试用例CloverCase
        CloverCase = type('TestCloverCase_' + str(i), (unittest.TestCase,), {})
        test_method = _make_test(case)
        setattr(CloverCase, 'test_' + str(i), test_method)
        # loader对象的loadTestsFromTestCase会返回一个suite对象
        test_case = loader.loadTestsFromTestCase(CloverCase)
        suite.addTest(test_case)
    # 使用runner运行suite
    path = os.path.join(os.getcwd(), 'logs', 'Clover测试报告.html')
    report = open(path, 'w', encoding='utf-8')
    runner = HTMLTestRunner(
        stream=report,
        verbosity=2,
        title='Clover测试报告',
        description='Clover测试报告-HTMLTestRunner版'
    )
    result = runner.run(suite)
    report.close()
    return result
