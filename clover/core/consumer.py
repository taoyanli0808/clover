import time

from clover.core.context import Context
from clover.core.executor import Executor
from clover.exts import client


class Consumer():

    def __init__(self):
        self.client = client
        self.executor = Executor()
        self.context = Context()

    def stream_consumer(self, *args, **kwargs):
        """
        stream消费者
        *args: 预留1.stream名称；2.group名称；3.consumer名称
        **kwargs: Still not ready yet
        TODO:
            1. ack后给外层提供一个回调函数       on_success()
            2. 异步任务执行失败后提供一个回调函数  on_failure()
            3. 异步任务重试时提供一个回调函数     on_retry()
            4. 增加独立日志
        """
        last_id = '0-0'
        check_backlog = True
        while True:
            if check_backlog:
                consumer_id = last_id
            else:
                consumer_id = '>'

            items = self.client.xreadgroup(
                'group_clover',
                'consumer_name',
                {'clover': consumer_id},
                block=0,
                count=10
            )
            print(self.client.xpending('clover', 'group_clover'))
            if not items:  # 处理空消息
                print('Timeout')
                print('Info Stream: {}'.format(self.client.xinfo_stream('clover')))
                print('Info Group: {}'.format(self.client.xinfo_groups('group_clover')))
                print('Info consumer: {}'.format(self.client.xinfo_consumers('clover', 'group_clover')))
                continue

            print(len(items[0][1]))
            check_backlog = False if len(items[0][1]) == 0 else True
            for id, fields in items[0][1]:
                print('Info: {0} {1} {2}'.format('consumer_name', id, fields))
                try:
                    print('...开始执行业务任务...')
                    self.context.build_context(fields)
                    self.executor.execute(self.context)
                    print('...业务任务执行完毕...')
                except Exception as e:
                    print(e)
                    continue
                else:
                    flag = self.client.xack('clover', 'group_clover', id)
                    print(self.client.xpending('clover', 'group_clover'))
                    if flag == 1:
                        self.client.xdel('clover', id)
                finally:
                    last_id = id

            time.sleep(1)  # 轮询间隔，目前无意义，需等加入线程运行后才可用
