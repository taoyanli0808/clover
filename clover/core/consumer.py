import json
import time

from clover.core.context import Context
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

    # TODO 消费者组,待优化
    # def stream_consumer(self):
    #     """
    #     stream消费者
    #     *args: 预留1.stream名称；2.group名称；3.consumer名称
    #     **kwargs: Still not ready yet
    #     TODO:
    #         1. ack后给外层提供一个回调函数       on_success()
    #         2. 异步任务执行失败后提供一个回调函数  on_failure()
    #         3. 异步任务重试时提供一个回调函数     on_retry()
    #         4. 增加独立日志
    #     """
    #     last_id = '0-0'
    #     check_backlog = True
    #     while True:
    #         if check_backlog:
    #             consumer_id = last_id
    #         else:
    #             consumer_id = '>'
    #
    #         items = self.client.xreadgroup(
    #             'group_clover',
    #             'consumer_name',
    #             {'clover': consumer_id},
    #             block=0,
    #             count=10
    #         )
    #         print(self.client.xpending('clover', 'group_clover'))
    #         if not items:  # 处理空消息
    #             print('Timeout')
    #             print('Info Stream: {}'.format(self.client.xinfo_stream('clover')))
    #             print('Info Group: {}'.format(self.client.xinfo_groups('group_clover')))
    #             print('Info consumer: {}'.format(self.client.xinfo_consumers('clover', 'group_clover')))
    #             continue
    #
    #         print(len(items[0][1]))
    #         check_backlog = False if len(items[0][1]) == 0 else True
    #         for id, fields in items[0][1]:
    #             print('Info: {0}, 异步任务ID: {1}'.format('consumer_name', id))
    #             if not fields['businessData']:
    #                 print(fields['businessData'])
    #                 continue
    #             try:
    #                 print('...开始执行业务任务...')
    #                 self.context.build_context(json.loads(fields['businessData']))
    #                 self.executor.execute(self.context)
    #                 print('...业务任务执行完毕...')
    #             except Exception as e:
    #                 print(e)
    #                 # 暂时无重试机制，但是下次重新启动worker时会再次运行pending中的任务
    #                 # TODO: 1.重试；2.重试次数超过3后从pending中移除
    #                 continue
    #             else:
    #                 flag = self.client.xack('clover', 'group_clover', id)
    #                 print(self.client.xpending('clover', 'group_clover'))
    #                 # if flag == 1:  # 暂不做删除，TODO：配置队列最大长度，超过max后自动删除已消费键值
    #                 #     self.client.xdel('clover', id)
    #             finally:
    #                 last_id = id
    #
    #         time.sleep(1)  # 轮询间隔，目前无意义，需等加入线程运行后才可用
