from typing import TYPE_CHECKING, Any, Self

from pymongo import MongoClient

from homelife.conf import conf

if TYPE_CHECKING:
    from pymongo.collection import Collection
    from pymongo.database import Database


class MongoDBClient:
    _instance: Self | None = None

    def __new__(cls, *args, **kwargs) -> Self:  # type: ignore
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
        return cls._instance

    def __init__(
        self, host: str, port: int, username: str, password: str, database_name: str
    ) -> None:
        uri: str = f"mongodb://{username}:{password}@{host}:{port}/"

        self.client: MongoClient[Any] = MongoClient(uri)
        self.database: "Database[Any]" = self.client[database_name]

    def collection(self, collection_name: str) -> "Collection[Any]":
        return self.database[collection_name]

    def close(self) -> None:
        self.client.close()


def get_mongo_client(
    conf: dict[str, Any] = conf,
) -> MongoDBClient:
    config: dict[str, Any] = conf["mongo"]
    return MongoDBClient(
        config["host"],
        config["port"],
        config["username"],
        config["password"],
        config["database"],
    )