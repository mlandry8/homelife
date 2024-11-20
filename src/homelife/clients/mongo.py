from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, host, port, username, password, database_name):
        uri = f"mongodb://{username}:{password}@{host}:{port}/"

        self.client = MongoClient(uri)
        self.database = self.client[database_name]

    def collection(self, collection_name):
        return self.database[collection_name]

    def close(self):
        self.client.close()
