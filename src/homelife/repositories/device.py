from typing import TYPE_CHECKING, Annotated, Any, Iterable

from fastapi import Depends

from homelife.clients.mongo import MongoDBClient, get_mongo_client
from homelife.models.device import Device, PostDevice
from homelife.models.location import Location
from homelife.repositories import Repository

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


class DeviceRepository(Repository):
    def __init__(self, db: "MongoDBClient") -> None:
        super().__init__(db, "devices")

    def intialise(self, device: Device | PostDevice) -> Device:
        db_device: Any | None = self.db.find_one(
            {"token": device.token, "status": "pending"}
        )

        if not db_device:
            raise Exception(f"No pending invite for token: {device.token}")

        self.db.update_one(
            {"_id": db_device["_id"]},
            {
                "$set": {
                    "device_id": device.device_id,
                    "status": "active",
                    "nickname": device.nickname,
                }
            },
        )

        resp_device = Device(**device.model_dump())
        resp_device.status = "active"
        return resp_device

    def retrieve_one(
        self,
        device_id: str | None = None,
        token: str | None = None,
        strict: bool = False,
    ) -> Device:
        device: dict[str, Any] | None = {}

        if (token and device_id) or strict:
            device = self.db.find_one({"token": token, "device_id": device_id})

        elif token or device_id:
            device = self.db.find_one(
                {"$or": [{"token": token}, {"device_id": device_id}]}
            )

        if not device:
            raise Exception(f"Device not found: {device_id}")

        return Device(**device)

    def retrieve_many(self) -> Iterable[Device]:
        for device in self.db.aggregate(
            [
                {"$match": {"status": "active"}},
                {
                    "$project": {
                        "device_id": 1,
                        "nickname": 1,
                        "token": 1,
                        "status": 1,
                        "locations": {
                            "$cond": {
                                "if": {
                                    "$ne": [{"$ifNull": ["$locations", None]}, None]
                                },
                                "then": [{"$arrayElemAt": ["$locations", -1]}],
                                "else": [],
                            }
                        },
                    }
                },
                {"$project": {"_id": 0}},
            ]
        ):
            yield Device(**device)


    def add_location(self, device: Device, location: Location) -> None:
        device.locations.append(location)
        self.db.update_one(
            {"device_id": device.device_id},
            {"$push": {"locations": location.model_dump()}},
        )


def get_device_repository(
    mongo_client: "MongoDBClient" = Depends(get_mongo_client),
) -> DeviceRepository:
    return DeviceRepository(mongo_client)


DeviceRepo = Annotated[DeviceRepository, Depends(get_device_repository)]
