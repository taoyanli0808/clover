
import datetime

from clover.common.utils import get_friendly_id
from clover.common.utils.mongo import Mongo


class Service():

    def __init__(self):
        self.db = Mongo()

    def create(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('_id', get_friendly_id())
        data.setdefault('created', datetime.datetime.now())
        id = self.db.insert("testsuite", "interface", data)
        return id

    def search(self, data):
        """
        :param data:
        :return:
        """
        count, results = self.db.search("testsuite", "interface", data)
        return (count, results) if results else (0, [])

    def trigger(self, data):
        """
        :param data:
        :return:
        """
        for case in data['cases']:
            _, result = self.db.search("interface", "case", {'_id': case['_id']})
            print(result)
