
from config import NOTIFY
from clover.common.wechat import WeChat
from clover.common.mail import send_email


def notify(data, events):
    """
    # 注意这个函数要保证每个渠道只发送一次通知
    # 如果多个event满足时只有一次触发即可
    :param data:
    :param events:
    :return:
    """
    for channel in NOTIFY['channel']:
        if channel == 'email':
            for event in NOTIFY['event']:
                if event in events:
                    send_email(data)
                    break
        if channel == 'wechat':
            for event in NOTIFY['event']:
                if event in events:
                    wechat = WeChat()
                    wechat.send_message(data)
                    break
