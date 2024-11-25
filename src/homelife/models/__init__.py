from typing import TYPE_CHECKING, Any

from pymongo.synchronous.collection import Collection

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


class Model:
    def __init__(self, db: MongoDBClient, collection: str) -> None:
        self.db: Collection[Any] = db.collection(collection)
