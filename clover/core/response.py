
from json import loads

import requests.Response

class Response(object):

    def __init__(self, response: requests.Response) -> None:
        self.status = response.status_code
        self.header = dict(response.headers)
        self.response = response.text
        try:
            self.json = loads(response.text)
        except Exception:
            self.json = {}
