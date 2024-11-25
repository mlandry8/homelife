from typing import TYPE_CHECKING, Any

from homelife.models import Model

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


class Devices(Model):
    def __init__(self, db: MongoDBClient, collection: str) -> None:
        super().__init__(db, collection)

        self.devices: list[Any] = []

    def retrieve(self) -> None:
        self.devices = list(
            self.db.aggregate(
                [
                    {"$match": {"status": "active"}},
                    {
                        "$project": {
                            "device_id": 1,
                            "nickname": 1,
                            "location": {"$arrayElemAt": ["$locations", -1]},
                        }
                    },
                    {"$project": {"_id": 0}},
                ]
            )
        )
