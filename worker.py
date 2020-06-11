"""
使用说明：
1. 先启动redis服务器
2. 启动python manage.py
3. 启动worker
    python worker.py  # 暂时不支持参数化启动

2020.6.12 目前处于测试阶段，有问题随时反馈issues

PS：调试、测试等请移步至 clover/test 单元测试

clover/core/message.py为消息队列的生产者
clover/core/consumer.py为消息队列的消费者
主目录/worker.py 要打造一个可分布式多线程消费的worker(对标celery的worker)
"""
import sys
import redis

from clover.core.consumer import Consumer
from clover.exts import client


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
        self.mq = Consumer()
        if client.xlen('clover') == 0:
            try:
                stream_id = client.xadd('clover', {'businessData': ''})
                client.xgroup_create('clover', 'group_clover', id=0)
            except redis.exceptions.ResponseError as e:  # redis.exceptions.ResponseError
                pass  # print(e)
            finally:
                client.xack('clover', 'group_clover', stream_id)
                client.xdel('clover', stream_id)
        super().__init__()

    def run(self):
        """
            TODO:
                1. 线程
                2. Click命令行传参
        """
        try:
            self.mq.stream_consumer()
        except KeyboardInterrupt:
            print(' 退出 Crtl + C ')
            sys.exit()


if __name__ == '__main__':
    myWorker().run()
