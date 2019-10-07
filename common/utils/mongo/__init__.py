
from pymongo import MongoClient

from config import DATABASE


class Mongo():

    def __init__(self, host=None, port=None):
        """
        :param host:
        :param port:
        """
        host = DATABASE['HOST'] if host is None else host
        port = DATABASE['PORT'] if port is None else port
        self.client = MongoClient(host, port)

    def insert(self, database, collection, documents):
        """
        :param database:
        :param collection:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        if isinstance(documents, list):
            result = _collection.insert_many(documents)
            return [str(id) for id in result.inserted_ids]
        else:
            result = _collection.insert_one(documents)
            return str(result.inserted_id)

    def delete(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        result = _collection.delete_many(filter)
        print(result)

    def update(self, database, collection, filter, document):
        """
        :param database:
        :param collection:
        :param filter:
        :param document:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        _collection.update_one(filter, {'$set': document})

    def search(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        results = list(_collection.find(filter))
        for result in results:
            result['_id'] = str(result['_id'])
        return results

    def close(self):
        """
        :return:
        """
        if self.client:
            self.client.close()

    def __del__(self):
        """
        :return:
        """
        if self.client:
            self.client.close()


if __name__ == '__main__':
    mongo = Mongo()
    result = mongo.insert("clover", "automation", {'name': 123})
    print(result)
    result = mongo.insert("clover", "automation", [{'name': 123}, {'name': 123}])
    print(result)
