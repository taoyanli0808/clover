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

from clover.core.consumer import Consumer


class myWorker(object):

    def __init__(self):
        self.mq = Consumer()
        super().__init__()

    def run(self):
        """
            TODO:
                1. 线程
                2. Click命令行传参
        """
        print('开始消费clover队列的消息......')
        print('redis队列模型为stream,消费模式为FIFO,消费方式XREAD \n')
        try:
            self.mq.read()
        except KeyboardInterrupt:
            print('主动退出 (Crtl+C)')
            sys.exit()


if __name__ == '__main__':
    myWorker().run()
