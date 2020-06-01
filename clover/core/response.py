
from json import loads

from urllib3.response import HTTPResponse

class Response(object):

    def __init__(self, response: HTTPResponse) -> None:
        self.status = response.status_code
        self.elapsed = response.elapsed
        self.header = dict(response.headers)
        self.response = response.text
        try:
            self.json = loads(response.text)
        except Exception:
            self.json = {}
