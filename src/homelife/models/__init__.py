from homelife.clients.mongo import MongoDBClient


class Model:
    def __init__(self, db: MongoDBClient, collection: str):
        self.db = db.collection(collection)
