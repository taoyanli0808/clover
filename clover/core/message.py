"""
# 不在使用celery，使用redis简单传递数据，后续会进一步优化。
"""
import json
import time
import uuid

import redis

import config

from clover.common import CloverJSONEncoder, get_timestamp


class Message(object):

    def __init__(self):
        self.client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DATABASE,
            decode_responses=True,
        )
        self.ps = self.client.pubsub()

    def send(self, data):
        """
        :param data:
        :return:
        """
        redis_data = {
            'uuid': '',
            'enter_queue_time': '',
            'business_data': {},
            'retry': 1
        }
        if 'uuid' in redis_data:
            # 任务进入队列次数 >=2
            redis_data.setdefault('enter_queue_time', get_timestamp())
            if 'retry' in redis_data:
                # 任务进入队列次数 >= 3
                redis_data.setdefault('retry', redis_data.get('retry') + 1)
            else:
                # 任务进入队列次数 == 2
                redis_data.setdefault('retry', 1)
        else:
            # 任务进入队列次数 == 1
            redis_data = {'business_data': data}
            redis_data.setdefault('uuid', str(uuid.uuid1()))
            redis_data.setdefault('enter_queue_time', get_timestamp())

        if isinstance(redis_data['business_data'], dict):
            redis_data = json.dumps(redis_data, cls=CloverJSONEncoder)
        else:
            return
        # lpush 插入新消息
        self.client.rpush('clover', redis_data)

    def receive(self):
        """
        :return:
        """
        # brpop 消费消息(阻塞模式：传统观察者模式)(消息键值也被删除)
        # 优点：阻塞读在队列没有数据的时候进入休眠状态，一旦数据到来则立刻醒过来，消息延迟几乎为零
        # 缺点：空闲连接的问题，Redis客户端的连接就成了闲置连接，闲置过久，服务器一般会主动断开连接，减少闲置资源占用，这个时候blpop和brpop或抛出异常，所以在编写客户端消费者的时候要小心，如果捕获到异常，还有重试。
        data = self.client.blpop('clover')
        # data返回为元组('clover', '{"key": "value"}')
        return json.loads(data[1]) if data[1] else None

    def ack(self):
        # TODO
        pass

    def broadcast(self, data):
        if isinstance(data, dict):
            data = json.dumps(data, cls=CloverJSONEncoder)
        else:
            return
        self.client.publish('clover_channel', data)

    def listen(self):
        self.ps.subscribe('clover_channel')
        for item in self.ps.listen():
            if item['type'] == 'message':
                return item['data']

    def send_stream(self, data):
        print('send mes into stream:')
        self.client.xadd('clover', data)
        print(self.client.xinfo_stream('clover'))
        try:
            self.client.xgroup_create('clover', 'group_clover', id=0)
            print(self.client.xinfo_groups('clover'))
        except Exception as e:  # redis.exceptions.ResponseError
            print(e)

    def stream_consumer(self):
        # while True:
        #     data = self.client.xread({'clover': '$'}, block=0)
        #     print('stream is name: {}'.format(data[-1][0]))
        #     for i in data[-1][1]:
        #         print('data is {}'.format(i))

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
            if not items:  # 如果 block 不是 0或者为空, 会需要这段
                print('Timeout')
                print('Info Stream: {}'.format(self.client.xinfo_stream('clover')))
                print('Info Group: {}'.format(self.client.xinfo_groups('group_clover')))
                print('Info consumer: {}'.format(self.client.xinfo_consumers('clover', 'group_clover')))
                continue

            print(len(items[0][1]))
            check_backlog = False if len(items[0][1]) == 0 else True
            for id, fields in items[0][1]:
                print('Info: {0} {1}={2}'.format('consumer_name', id, fields))
                try:
                    print('执行函数')
                    time.sleep(3)
                    print('end...')
                except Exception as e:
                    print(e)
                    continue
                finally:
                    last_id = id
                flag = self.client.xack('clover', 'group_clover', id)
                print(self.client.xpending('clover', 'group_clover'))
                # if flag == 1:
                #     self.client.xdel('clover', id)

            time.sleep(5)  # 轮询间隔


if __name__ == '__main__':
    data1 = {'a': 1, 'b': 2}
    data2 = {'c': 2, 'd': [4, 5]}
    message = Message()
    message.send(data1)
    message.send(data2)
    print(message.receive())
    print(message.receive())
