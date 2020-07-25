import json

import requests

from clover.config import NOTIFY
from clover.config import DOMAIN


class Dingtalk(object):

    def __init__(self):
        self.url = "https://oapi.dingtalk.com"

    def send_message(self, data):
        '''
        url需要更改为自己的群机器人Webhook.singleURL也需要修改
        :param report_rul:
        :return:
        '''
        data.setdefault('domain', DOMAIN)
        url = self.url + "/robot/send?access_token={}".format(NOTIFY['channel']['dingtalk'])
        header = {
            'Content-Type': 'application/json'
        }
        payload = {
            "actionCard": {
                "title": "clover平台通知",
                "text": "接口自动化测试报告",
                "btnOrientation": "0",
                "singleTitle": "查看报告详情",
                "singleURL": "{domain}/report/detail?id={id}".format(**data)
            },
            "msgtype": "actionCard"
        }
        requests.request('POST', url, data=json.dumps(payload), headers=header)


if __name__ == '__main__':
    data = {
        'id': 2,
        'type': 'interface',
        'team': '质量部',
        'project': 'clover测试平台',
        'name': '变量和断言',
        'interface': {
            'total': 1,
            'verify': 2,
            'percent': '100.0%',
        },
        'start': '2020-01-17 17:24:00',
        'end': '2020-01-17 17:24:00',
    }
    dingtalk = Dingtalk()
    dingtalk.send_message(data)
