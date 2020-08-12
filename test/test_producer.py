import unittest
import time

from clover.core.producer import Producer
from clover.core.consumer import Consumer
from clover.interface.service import a


class TestMessage(unittest.TestCase):

    def setUp(self) -> None:
        self.mq = Producer()
        self.cm = Consumer()

    def test_send(self):
        # for i in range(10):
        #     self.mq.send({'test': i})
        #     print(i)
        #     time.sleep(1)

        data = {'report': 'test11', 'body': None, 'created': '2020-01-09 00:20:25', 'enable': 0,
                'extract': [{'expected': '', 'expression': '', 'selector': ''}], 'header': [{'key': '', 'value': ''}],
                'host': 'http://ip.taobao.com', 'id': 1, 'method': 'get', 'name': 'test1淘宝接口',
                'params': [{'key': 'ip', 'value': '63.223.108.42'}], 'path': '/service/getIpInfo.php',
                'project': '人脸识别', 'sub_type': 'None', 'team': '计算机视觉', 'type': 'None', 'updated': '2020-01-11 14:58:32',
                'verify': [{'comparator': '', 'convertor': '', 'expected': '', 'expression': '', 'extractor': ''}]}
        for i in range(10):
            self.mq.send(data)
            time.sleep(0.1)
            a(i)

    def test_read(self):
        self.cm.read()
        time.sleep(1)

    def tearDown(self) -> None:
        pass
