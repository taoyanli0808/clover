"""
# https://github.com/cameronmaske/celery-once
"""

from celery_once import QueueOnce

from config import NOTIFY
from clover.exts import task
from clover.common import get_system_info
from clover.common.executor import Executor
from clover.report.service import ReportService
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


@task.task(base=QueueOnce, once={'graceful': True})
def interface_task(cases, data):
    from clover import app

    with app.test_request_context():
        print("What？！")
        executor = Executor()
        executor.execute(cases, data)

        # events = 'success' if executor.interface['passed'] == executor.interface['total'] else 'failed'
        # notify(update_report, events)

    return 1
