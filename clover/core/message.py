"""
# 不在使用celery，使用redis简单传递数据，后续会进一步优化。
"""
import json

import redis

import config

from clover.common import CloverJSONEncoder

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
        self.client.rpush('clover', json.dumps(data, cls=CloverJSONEncoder))

    def receive(self):
        """
        :return:
        """
        data = self.client.lpop('clover')
        return None if data is None else json.loads(data)


if __name__ == '__main__':
    data1 = {'a': 1, 'b': 2}
    data2 = {'c': 2, 'd': [4, 5]}
    message = Message()
    message.send(data1)
    message.send(data2)
    print(message.receive())
    print(message.receive())
