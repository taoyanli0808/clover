import json
import time

from clover.core.case import Context
from clover.core.executor import Executor
from clover.exts import client


class Consumer(object):

    def __init__(self):
        self.client = client
        self.executor = Executor()
        self.context = Context()

    def read(self):
        while True:
            # XREAD() 阻塞式读取消息
            items = self.client.xread(
                {'clover': '0-0'},  # FIFO消费方式消费队列
                block=0,  # 阻塞式消费
                count=1   # xread每次从消息队列最多取一个消息
            )
            stream_id = items[0][1][0][0]
            fields = items[0][1][0][1]
            data = json.loads(fields['businessData'])
            try:
                print(f'{stream_id}消息 开始消费...')
                self.context.build_context(data)
                self.executor.execute(self.context)
            except Exception as e:
                print(f'{stream_id}消息消费失败; 暂无重试机制,请修改业务代码bug后重新发消息消费')
                print(e)
                self.client.xdel('clover', stream_id)
            else:
                print(f'{stream_id}消息消费成功')
                self.client.xdel('clover', stream_id)

            # 消费频率，监听队列间隔，轮询间隔
            time.sleep(1)
