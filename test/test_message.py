import unittest
import time

from clover.core.message import Message


class TestMessage(unittest.TestCase):
    def setUp(self) -> None:
        self.mq = Message()

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

    def test_listen(self):
        while True:
            print(self.mq.listen())

    def test_stream(self):
        for i in range(120, 130):
            self.mq.send_stream({'test': i})

    def test_stream_consumer(self):
        self.mq.stream_consumer()

    def tearDown(self) -> None:
        pass
