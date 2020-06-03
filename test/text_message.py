import unittest
import time
from clover.core.message import Message


class TestMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.mq = Message()

    def test_send(self):
        msg_int = 1
        while True:
            print("发送消息：{}".format(msg_int))
            self.mq.send({msg_int: msg_int})
            msg_int += 1
            time.sleep(1)

    def test_receive1(self):
        msg_int = 1
        while True:
            data = self.mq.receive()
            print("获取消息：{}".format(data))
            msg_int += 1
            time.sleep(1)

    def test_receive2(self):
        msg_int = 1
        while True:
            data = self.mq.receive()
            print("获取消息：{}".format(data))
            msg_int += 1
            time.sleep(1)

    def tearDown(self) -> None:
        pass
