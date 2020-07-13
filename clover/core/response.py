
from json import loads

from urllib3.response import HTTPResponse


class Response(object):

    def __init__(self, response: HTTPResponse) -> None:
        self.status = response.status_code if response is not None else None
        if response is not None:
            self.elapsed = float("{}.{}".format(response.elapsed.seconds, response.elapsed.microseconds))
        else:
            self.elapsed = 0.0
        self.header = dict(response.headers) if response is not None else {}
        self.response = response.text if response is not None else ''
        try:
            self.json = loads(response.text)
        except Exception:
            self.json = {}

    def get_response(self):
        return {
            'status': self.status,
            'elapsed': self.elapsed,
            'header': self.header,
            'content': self.response,
            'json': self.json,
        }
