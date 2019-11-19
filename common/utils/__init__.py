
import time
import uuid


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
