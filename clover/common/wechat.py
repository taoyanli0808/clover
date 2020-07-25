
import requests

from clover.config import NOTIFY
from clover.config import DOMAIN

# 企业微信配置
WECHAT = {
    'key': 'wechat_key',
    'template': {
        'msgtype': 'markdown',
        'markdown': {
            'content': 'Clover平台运行报告！\n'+
            '>类型:<font color=\"comment\">{type}</font>\n' +
            '>团队:<font color=\"comment\">{team}</font>\n' +
            '>项目:<font color=\"comment\">{project}</font>\n' +
            '>名称:<font color=\"comment\">{name}</font>\n' +
            '>接口:<font color=\"comment\">{interface[total]}个</font>\n' +
            '>断言:<font color=\"comment\">{interface[verify]}个</font>\n' +
            '>成功率:<font color=\"comment\">{interface[percent]}</font>\n' +
            '>开始时间:<font color=\"comment\">{start}</font>\n' +
            '>结束时间:<font color=\"comment\">{end}</font>\n' +
            '[测试报告-{id}]({domain}/report/detail?id={id})'
        }
    }
}


class WeChat(object):

    def __init__(self):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin"

    def send_message(self, data):
        """
        # https://work.weixin.qq.com/api/doc/90000/90135/90235
        :param data:
        :return:
        """
        WECHAT['key'] = NOTIFY['channel']['wechat']
        url = self.url + '/webhook/send?key=' + WECHAT['key']

        data.setdefault('domain', DOMAIN)
        WECHAT['template']['markdown']['content'] = WECHAT['template']['markdown']['content'].format(**data)
        try:
            print(url, WECHAT['key'])
            response = requests.post(url, json=WECHAT['template'])
            if response.status_code == 200:
                result = response.json()
                print(result)
        except Exception:
            return None


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
    wechat = WeChat()
    wechat.send_message(data)