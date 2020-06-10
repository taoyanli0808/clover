import logging
from clover.core.message import Message


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
        super().__init__()

    def run(self):
        """
            TODO:
                1. 线程
                2. Click命令行传参
        """
        self.mq.stream_consumer()


if __name__ == '__main__':
    myWorker().run()
