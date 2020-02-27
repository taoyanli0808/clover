
import requests

from config import WECHAT


class WeChat(object):

    def __init__(self):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin"

    def send_message(self, data):
        """
        # https://work.weixin.qq.com/api/doc/90000/90135/90235
        :param data:
        :return:
        """
        url = self.url + '/webhook/send?key=' + WECHAT['key']
        template = WECHAT['template']
        template['markdown']['content'] = template['markdown']['content'].format(**data)
        try:
            response = requests.post(url, json=template)
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
        'interface': 1,
        'verify': 2,
        'percent': '100.0%',
        'start': '2020-01-17 17:24:00',
        'end': '2020-01-17 17:24:00',
    }
    wechat = WeChat()
    wechat.send_message(data)