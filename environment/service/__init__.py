
from common.utils.mongo import Mongo
from common.utils import get_friendly_id


class Service():

    def __init__(self):
        self.db = Mongo()

    def create(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('_id', get_friendly_id())
        return self.db.insert("variable", "variable", data)

    def detele(self, data):
        """
        :param data:
        :return:
        """
        count = 0
        for id in data['id_list']:
            result = self.db.delete("variable", "variable", {'_id': id})
            count += result
        return count

    def update(self, data):
        """
        :param data:
        :return:
        """
        filter = {'_id': data.pop('_id')}
        return self.db.update("variable", "variable", filter, data)

    def search(self, data):
        """
        :param data:
        :return:
        """
        return self.db.search("variable", "variable", data)
