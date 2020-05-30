
import time

from clover.core.message import Message
from clover.common.executor import Executor

class Worker(object):

    def __init__(self):
        self.message = Message()
        self.executor = Executor()

    def run(self):
        while True:
            data = self.message.receive()
            if data is None:
                print("接收到空数据，等待1秒钟后继续接收数据...")
                time.sleep(1.0)
                continue
            self.executor.execute(data['case'], data['data'])


if __name__ == '__main__':
    worker = Worker()
    worker.run()
