"""
# 不在使用celery，使用redis简单传递数据，后续会进一步优化。
"""
import json
import time

import redis

import config

from clover.common import CloverJSONEncoder, get_timestamp


class Message(object):

    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DATABASE,
            decode_responses=True
        )

    def send(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('timestamp', time.time())
        # json序列化
        try:
            if isinstance(dict, data):
                data = json.dumps(data, cls=CloverJSONEncoder)
            else:
                return
        except Exception as e:
            print(e)
            return
        # lpush 插入新消息
        self.client.rpush('clover', data)

    def receive(self):
        """
        :return:
        """
        # brpop 消费消息(阻塞模式：传统观察者模式)(消息键值也被删除)
        # 优点：阻塞读在队列没有数据的时候进入休眠状态，一旦数据到来则立刻醒过来，消息延迟几乎为零
        # 缺点：空闲连接的问题，Redis客户端的连接就成了闲置连接，闲置过久，服务器一般会主动断开连接，减少闲置资源占用，这个时候blpop和brpop或抛出异常，所以在编写客户端消费者的时候要小心，如果捕获到异常，还有重试。
        data = self.client.blpop('clover')
        # data返回为元组('clover', '{"key": "value"}')
        return json.loads(data[1]) if data[1] else None
    
    def ack(self):
        # TODO
        pass


if __name__ == '__main__':
    data1 = {'a': 1, 'b': 2}
    data2 = {'c': 2, 'd': [4, 5]}
    message = Message()
    message.send(data1)
    message.send(data2)
    print(message.receive())
    print(message.receive())
