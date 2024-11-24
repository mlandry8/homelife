from typing import TYPE_CHECKING, Any

from pymongo import MongoClient

if TYPE_CHECKING:
    from pymongo.collection import Collection
    from pymongo.database import Database


class MongoDBClient:
    def __init__(
        self, host: str, port: int, username: str, password: str, database_name: str
    ) -> None:
        uri: str = f"mongodb://{username}:{password}@{host}:{port}/"

        self.client: MongoClient[Any] = MongoClient(uri)
        self.database: Database[Any] = self.client[database_name]

    def collection(self, collection_name: str) -> Collection[Any]:
        return self.database[collection_name]

    def close(self) -> None:
        self.client.close()
