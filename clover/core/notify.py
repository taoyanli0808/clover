
from clover.config import NOTIFY
from clover.common.wechat import WeChat
from clover.common.dingtalk import Dingtalk
from clover.common.mail import send_email


class Notify():

    def __init__(self): pass

    def send_message(self, data, event):
        """
        # 注意这个函数要保证每个渠道只发送一次通知
        # 如果多个event满足时只有一次触发即可
        :param data:
        :param event:
        :return:
        """
        for channel in NOTIFY['channel']:

            print(channel, event)

            if channel == 'email':
                for evt in NOTIFY['event']:
                    if evt == event:
                        try:
                            send_email(data)
                            break
                        except Exception:
                            pass

            if channel == 'wechat':
                for evt in NOTIFY['event']:
                    if evt in event:
                        try:
                            wechat = WeChat()
                            wechat.send_message(data)
                            break
                        except Exception:
                            pass

            if channel == 'dingtalk':
                for evt in NOTIFY['event']:
                    if evt in event:
                        try:
                            dingtalk = Dingtalk()
                            dingtalk.send_message(data)
                            break
                        except Exception:
                            pass
