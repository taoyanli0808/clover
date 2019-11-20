
from clover.common.utils.mongo import Mongo
from clover.common.utils import get_friendly_id


class Service():

    def __init__(self):
        self.db = Mongo()

    def create(self, data):
        """
        :param data:
        :return:
        """
        data.setdefault('_id', get_friendly_id())
        collection = data.get("type", None)
        return self.db.insert("environment", collection, data)

    def detele(self, data):
        """
        :param data:
        :return:
        """
        count = 0
        collection = data.get("type", None)
        for id in data['id_list']:
            result = self.db.delete("environment", collection, {'_id': id})
            count += result
        return count

    def update(self, data):
        """
        :param data:
        :return:
        """
        filter = {'_id': data.pop('_id')}
        collection = data.get("type", None)
        return self.db.update("environment", collection, filter, data)

    def search(self, data):
        """
        :param data:
        :return:
        """
        collection = data.pop("type", None)
        result = self.db.search("environment", collection, data)
        return result

    def aggregate(self, data):
        """
        :param data:
        :return:
        """
        collection = data.pop("type", None)
        key = data.pop("key", None)
        pipeline = [
            {'$group': {'_id': "$" + key}},
        ]
        return self.db.aggregate("environment", collection, pipeline)
