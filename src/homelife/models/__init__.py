from typing import Any
from pymongo.synchronous.collection import Collection
from homelife.clients.mongo import MongoDBClient


class Model:
    def __init__(self, db: MongoDBClient, collection: str) -> None:
        self.db: Collection[Any] = db.collection(collection)
