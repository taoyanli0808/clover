
import datetime

from clover.common.utils import get_friendly_id
from clover.common.utils.mongo import Mongo

class Service():

    def __init__(self):
        self.db = Mongo()

    def create(self, data):
        data.setdefault('_id', get_friendly_id())
        data.setdefault('created', datetime.datetime.now())
        id = self.db.insert("testsuite", "interface", data)
        return id

    def search(self, data):
        count, results = self.db.search("testsuite", "interface", data)
        return (count, results) if results else (0, [])
