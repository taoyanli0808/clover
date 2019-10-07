
import time
import uuid
import json

from kafka import KafkaProducer
from kafka import KafkaConsumer

from config import KAFKA


def get_timestamp(data=None, format="%Y-%m-%d %H:%M:%S"):
    """
    :param data:
    :param format:
    :return:
    """
    if data is None:
        data = time.time()
    return time.strftime(format, time.localtime(data))


def get_friendly_id():
    """
    采用时间加uuid随机部分作为可读性高的ID来使用。
    :return:
    """
    stamp = get_timestamp(format="%Y%m%d%H%M%S")
    uid = str(uuid.uuid1()).replace('-', '')
    return stamp + '_' + uid[4:8] + uid[16:20]


def sender(data):
    producer = KafkaProducer(bootstrap_servers=KAFKA['SERVER'],
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(KAFKA['TOPIC'], data, partition=0)
    producer.close()


def receiver(callback):
    """
    :return:
    """
    consumer = KafkaConsumer(KAFKA['TOPIC'], bootstrap_servers=KAFKA['SERVER'])
    for msg in consumer:
        recv = "%s:%d:%d: key=%s value=%s" % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
        print(recv)
        data = json.loads(msg.value)
        if not callable(callback):
            raise Exception("callback should be callable.")
        callback(data)


if __name__ == '__main__':
    # sender({
    #     'status': 0,
    #     'message': 'ok',
    #     'data': [{'a': 1}, {'b': 2}]
    # })
    receiver(print)
