
from json import loads

from requests.utils import dict_from_cookiejar


class Response(object):

    def __init__(self):
        self.status = 0
        self.reason = ''
        self.elapsed = 0.0
        self.header = {}
        self.response = ''
        self.cookies = {}
        self.json = {}
        self.start = 0.0
        self.end = 0.0

    def set_response(self, response):
        self.status = response.status_code if response is not None else None
        self.reason = response.reason if response is not None else None
        if response is not None:
            self.elapsed = float("{}.{}".format(response.elapsed.seconds, response.elapsed.microseconds))
        else:
            self.elapsed = 0.0
        self.header = dict(response.headers) if response is not None else {}
        self.response = response.text if response is not None else ''
        self.cookies = dict_from_cookiejar(response.cookies) if response is not None else {}
        try:
            self.json = loads(response.text)
        except Exception:
            self.json = {}

    def get_response(self):
        # 有必要保留么？
        return {
            'status': self.status,
            'reason': self.reason,
            'elapsed': self.elapsed,
            'header': self.header,
            'cookie': self.cookies,
            'content': self.response,
            'json': self.json,
        }
