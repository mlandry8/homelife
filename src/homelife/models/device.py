from homelife.models import Model
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


class Device(Model):
    def __init__(
        self,
        db: MongoDBClient,
        collection: str,
        device_id: str | None = None,
        token: str | None = None,
    ):
        super().__init__(db, collection)

        self.device_id: str | None = device_id
        self.token: str | None = token
        self.status: str | None = None
        self.nickname: str | None = None
        self.locations: list[Any] = []

    def _set(self, device: Any) -> None:
        self.device_id = device.get("device_id")
        self.token = device.get("token")
        self.status = device.get("status")
        self.nickname = device.get("nickname")
        self.locations = device.get("locations", [])

    def is_set(self) -> bool:
        return bool(self.device_id and self.token)

    def intialise(self, token: str, device_id: str, nickname: str) -> None:
        device: Any | None = self.db.find_one({"token": token, "status": "pending"})

        if not device:
            raise Exception(f"No pending invite for token: {token}")

        device["device_id"] = device_id
        device["nickname"] = nickname
        device["status"] = "active"

        self.db.update_one(
            {"_id": device["_id"]},
            {
                "$set": {
                    "device_id": device_id,
                    "status": "active",
                    "nickname": nickname,
                }
            },
        )

        self._set(device)

    def retrieve(self, device_id: str | None = None, token: str | None = None) -> None:
        device_id = device_id or self.device_id
        token = token or self.token

        device: Any | None = None

        if token and device_id:
            device = self.db.find_one({"token": token, "device_id": device_id})

        elif token or device_id:
            device = self.db.find_one(
                {"$or": [{"token": token}, {"device_id": device_id}]}
            )

        self._set(device or {})

    def add_location(self, location: Any) -> None:
        self.locations.append(location)
        self.db.update_one(
            {"device_id": self.device_id}, {"$push": {"locations": location}}
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "device_id": self.device_id,
            "nickname": self.nickname,
            "status": self.status,
            "locations": self.locations,
        }

    def __str__(self) -> str:
        return f"{self.device_id} - {self.nickname}"
