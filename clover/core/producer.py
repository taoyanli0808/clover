"""
# 不在使用celery，使用redis简单传递数据，后续会进一步优化。
"""
import json

import redis

from clover.common import CloverJSONEncoder, get_timestamp
from clover.exts import client


class Producer(object):

    def __init__(self):
        self.client = client
        self.ps = self.client.pubsub()

    def send_stream(self, data, *args, **kwargs):
        """
        stream 生产者
        data: 暂定业务数据
        *args: 预留1.stream名称；2.group名称
        **kwargs: Still not ready yet
        return: 消息队列id
        TODO:
            1. 增加独立日志
        """
        try:
            # print('start send msg into stream:')
            stream_id = self.client.xadd('clover', {'businessData': json.dumps(data, cls=CloverJSONEncoder)})
            # print(self.client.xinfo_stream('clover'))
            self.client.xgroup_create('clover', 'group_clover', id=0)
        except redis.exceptions.ResponseError as e:  # redis.exceptions.ResponseError
            print('异步任务id: {}'.format(stream_id))
            print(self.client.xinfo_groups('clover'))
            return stream_id
        except Exception as e:
            print(e)
            return None
        else:
            print('异步任务id: {}'.format(stream_id))
            print(self.client.xinfo_groups('clover'))
            return stream_id
