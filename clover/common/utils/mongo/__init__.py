
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
        # print(database, collection, filter)
        result = _collection.delete_many(filter)
        # print(result.deleted_count)
        return result.deleted_count

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
        print(filter, document)
        result = _collection.update_one(filter, {'$set': document})
        return result.modified_count

    def search(self, database, collection, filter):
        """
        :param database:
        :param collection:
        :param filter:
        :return:
        """
        try:
            skip = int(filter.pop('skip'))
        except TypeError:
            skip = 0
        except KeyError:
            skip = 0

        try:
            limit = int(filter.pop('limit'))
        except TypeError:
            limit = 0
        except KeyError:
            limit = 0

        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        results = _collection.find(filter, skip=skip, limit=limit)
        count = _collection.count_documents(filter)
        results = list(results)

        return count, results

    def aggregate(self, database, collection, pipeline):
        _database = self.client.get_database(database)
        _collection = _database.get_collection(collection)
        return list(_collection.aggregate(pipeline))

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
