"""
# 不在使用celery，使用redis简单传递数据，后续会进一步优化。
"""
import json

from clover.common import CloverJSONEncoder
from clover.exts import client


class Producer(object):

    def __init__(self):
        self.client = client

    def send(self, data):
        """
        data: 暂定业务数据
        return: 消息队列id
        TODO:
            1. 增加独立日志
        """
        try:
            data = json.dumps(data, cls=CloverJSONEncoder)
            stream_id = self.client.xadd('clover', {'businessData': data})
        except Exception as e:
            print('消息发送失败, 请检查Redis版本是否为5.0以上,服务是否开启')
            print(e)
            return None
        else:
            print(f'{stream_id}消息发送成功')
            return stream_id
