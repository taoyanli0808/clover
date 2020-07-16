"""
使用说明：
1. 先启动redis服务器
2. 启动python manage.py
3. 启动worker
    python worker.py -h
    python worker.py (PS: 默认不带参数运行，主机名hostname将作为消费组的名称，消费者名称随机uuid1)
    python worker.py -C 'consumer_name' -G 'group_name'
目前：
    支持多worker运行，支持master-slave分布式模式运行
    一个worker 对应单个消费组并且只有一个消费者
TODO
    一个worker 对应单个消费者并且对应多个消费者
    一个worker 对应多个消费者并且对应多个消费者
    多队列+多worker模式(更完美的支持master-slave分布式)
"""

import sys
import json
import time
import uuid
import socket
import argparse

from redis import Redis

from clover.core.context import Context
from clover.core.executor import Executor
from config import REDIS_HOST, REDIS_PORT, REDIS_DATABASE, VERSION, REDIS_STREAM_NAME

try:
    redis = Redis(
        host=REDIS_HOST,  # localhost
        port=REDIS_PORT,  # 6379
        db=REDIS_DATABASE,  # 0
        decode_responses=True,
    )
except Exception as error:
    print(error)

stream_name = REDIS_STREAM_NAME

hostname = socket.gethostname()  # 默认的消费组名称设置为主机名


class Worker(object):

    def __init__(self):
        self.group = Groups()
        self.consumer = Consumers()
        super().__init__()

    def run(self, group_name, consumer_name):
        if not group_name:
            group_name = hostname
        if not consumer_name:
            consumer_name = str(uuid.uuid1())
        try:
            while True:  # stream队列不存在则5s轮询检查是否存在
                if redis.exists(stream_name) == 0:  # 0不存在，1存在
                    print(f'消息队列 {stream_name} 不存在...')
                    time.sleep(3)  # 轮询间隔5秒
                else:
                    break
        except KeyboardInterrupt:
            print('主动退出 (Crtl+C)')
            sys.exit()
        try:
            self.group.name = group_name
            print(f'消费者组名: {self.group.name}; 消费者名: {consumer_name}; 消息队列: {stream_name}')
            self.consumer.start_run(self.group.name, consumer_name)
        except KeyboardInterrupt:
            # 释放消费者
            self.consumer.delete(self.group.name, consumer_name)
            # 释放消费组
            # redis.xgroup_destroy(stream_name, group_name)
            print('主动退出 (Crtl+C)')
            sys.exit()


class Groups(object):
    """消费者组，返回组名"""

    def __init__(self):
        self.__name = hostname
        super().__init__()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, group_name):
        flag = False  # 消费者是否存在
        for item in redis.xinfo_groups(stream_name):
            if item.get('name') == group_name:
                flag = True
                break
        if not flag:
            redis.xgroup_create(stream_name, group_name, id=0)  # 创建消费者组，组名name
        self.__name = group_name

    @name.deleter
    def name(self):
        del self.__name


class Consumers(object):

    def __init__(self):
        self.executor = Executor()
        self.context = Context()
        super().__init__()

    def start_run(self, group_name, consumer_name):
        last_id = '0-0'  # 从0-0开始遍历stream，保证第一次遍历到所有消息
        check_backlog = True  # 判断消息遍历起点
        while True:
            # Pick the ID based on the iteration: the first time we want to
            # read our pending messages, in case we crashed and are recovering.
            # Once we consumer our history, we can start getting new messages.
            if check_backlog:
                stream_id = last_id
            else:
                stream_id = '>'
            items = redis.xreadgroup(
                group_name,
                consumer_name,
                {stream_name: stream_id},
                block=0,
                count=1  # 后续跟进程、线程数配合使用
            )
            if not items:  # 处理空消息
                print('Timeout')
                print('Info Stream: {} \n'.format(redis.xinfo_stream(stream_name)))
                print('Info Group: {} \n'.format(redis.xinfo_groups(group_name)))
                print('Info consumer: {} \n'.format(redis.xinfo_consumers(stream_name, group_name)))
                continue

            check_backlog = False if len(items[0][1]) == 0 else True
            for item_id, fields in items[0][1]:
                print(f'异步任务ID: {item_id}; 消息队列: {stream_name}; 消费者组名: {group_name}; 消费者名: {consumer_name}')
                if not fields['businessData']:
                    print(f'没有业务数据businessData: {fields}')
                    continue
                try:
                    print('...开始执行异步任务...')
                    self.context.build_context(json.loads(fields['businessData']))
                    self.executor.execute(self.context)
                    print('...异步任务执行完成...')
                except Exception as e:
                    print(e)
                    redis.xdel(stream_name, item_id)
                    redis.xadd(stream_name + '_fail', {'id': item_id, 'businessData': fields['businessData']},
                               maxlen=100)
                    # 如果不删除消息，下次重新启动worker时会再次运行pending中的任务（有重复执行的问题）
                    # TODO: 增加错误消息、死消息的监控处理（单独线程）。存在时间和统计次数两个维度判断死消息
                else:
                    flag = redis.xack(stream_name, group_name, item_id)
                    # if flag == 1:
                    #     self.client.xdel('clover', item_id)
                finally:
                    last_id = item_id

            time.sleep(1)  # 轮询间隔

    def delete(self, group_name, consumer_name):
        redis.xgroup_delconsumer(stream_name, group_name, consumer_name)


def main():
    parser = argparse.ArgumentParser()  # 初始化命令行 自带 --help 参数 缩写为-h
    # 可选参数 和 必填参数区别为 是否加 -
    parser.add_argument('-v', '--version', action='store_true', help='显示版本信息')
    parser.add_argument('-C', '--consumer',
                        help='消费者名称。默认为str(uuid1)自动生成',
                        type=str)
    parser.add_argument('-G', '--group',
                        help='消费组名称。默认为PC主机名(自动生成)',
                        type=str)
    # parser.add_argument('-S', '--streams',
    #                     help='消息队列名称。默认为clover, TIP:2.0版本暂不支持多队列形式',
    #                     type=str)

    # 获取命令行参数
    args = parser.parse_args()
    if args.version:
        print(VERSION)
        sys.exit()
    obj = Worker()
    obj.run(args.group, args.consumer)


if __name__ == '__main__':
    main()
