import logging
from clover.core.message import Message
from clover.core.context import Context
from clover.core.executor import Executor


class myWorker(object):

    # def __init__(self):
    #     self.message = Message()
    #     self.executor = Executor()
    #
    # def run(self):
    #     try:
    #         while True:
    #             data = self.message.receive()
    #             if data is None:
    #                 print("接收到空数据，等待1秒钟后继续接收数据...")
    #                 time.sleep(1.0)
    #                 continue
    #             context = Context()
    #             context.build_context(data)
    #             self.executor.execute(context)
    #     except KeyboardInterrupt:
    #         # self.message.send(data)
    #         print("用户中断，程序退出！")

    def __init__(self):
        self.mq = Message()
        self.executor = Executor()
        self.context = Context()
        super().__init__()

    def run(self):
        while True:
            # 1. 获取队列消息
            data = self.mq.receive()
            try:
                # 2. 解析参数
                if data['business_data']:
                    self.context.build_context(data['business_data'])
                    # 3. 执行指定函数
                    self.executor.execute(self.context)
            except Exception as e:
                self.mq.send(data)
                logging.error(e)

    def start(self):
        pass


if __name__ == '__main__':
    pass
