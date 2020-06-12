import json
import unittest
import time

from clover.core.producer import Producer
from clover.core.consumer import Consumer


class TestMessage(unittest.TestCase):

    def setUp(self) -> None:
        self.mq = Producer()
        self.work = Consumer()

    def test_send(self):
        msg_int = {'wewe': 1, "sdsd": '2020-2-2 13:04:09'}
        while True:
            print("发送消息：{}".format(msg_int))
            self.mq.send(msg_int)
            msg_int['wewe'] = msg_int['wewe'] + 1
            time.sleep(1)

    def test_receive1(self):
        while True:
            data = self.mq.receive()
            if data:
                print("获取消息：{}".format(data))

    def test_receive2(self):
        while True:
            data = self.mq.receive()
            print("获取消息：{}".format(data))

    def test_broadcast(self):
        # data = 1
        # while True:
        #     print('test_broadcast: {}'.format(data))
        #     self.mq.broadcast(data)
        #     data += 1
        #     time.sleep(1)
        self.mq.broadcast({'key': 8})

    def test_listen1(self):
        while True:
            print(self.mq.listen())

    def test_listen2(self):
        while True:
            print(self.mq.listen())

    def test_stream(self):
        # for i in range(120, 130):
        #     self.mq.send_stream({'test': i})

        data = {'report': 'test11', 'body': None, 'created': '2020-01-09 00:20:25', 'enable': 0,
                'extract': [{'expected': '', 'expression': '', 'selector': ''}], 'header': [{'key': '', 'value': ''}],
                'host': 'http://ip.taobao.com', 'id': 1, 'method': 'get', 'name': 'test1淘宝接口',
                'params': [{'key': 'ip', 'value': '63.223.108.42'}], 'path': '/service/getIpInfo.php',
                'project': '人脸识别', 'sub_type': 'None', 'team': '计算机视觉', 'type': 'None', 'updated': '2020-01-11 14:58:32',
                'verify': [{'comparator': '', 'convertor': '', 'expected': '', 'expression': '', 'extractor': ''}]}
        self.mq.send_stream({'test': json.dumps(data)})

    def test_stream_consumer(self):
        self.work.stream_consumer()

    def tearDown(self) -> None:
        pass
