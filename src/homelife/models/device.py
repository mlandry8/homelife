from homelife.models import Model


class Device(Model):
    def __init__(self, db, collection, device_id=None, token=None):
        super().__init__(db, collection)

        self.device_id: str = device_id
        self.token: str = token
        self.status: str = None
        self.nickname: str = None
        self.locations = []

    def _set(self, device):
        self.device_id = device.get("device_id")
        self.token = device.get("token")
        self.status = device.get("status")
        self.nickname = device.get("nickname")
        self.locations = device.get("locations", [])

    def is_set(self):
        return bool(self.device_id and self.token)

    def intialise(self, token, device_id, nickname=None):
        device = self.db.find_one({"token": token, "status": "pending"})

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

    def retrieve(self, device_id=None, token=None):
        device_id = device_id or self.device_id
        token = token or self.token

        if token and device_id:
            device = self.db.find_one({"token": token, "device_id": device_id})

        elif token or device_id:
            device = self.db.find_one(
                {"$or": [{"token": token}, {"device_id": device_id}]}
            )

        self._set(device or {})

    def add_location(self, location):
        self.locations.append(location)
        self.db.update_one(
            {"device_id": self.device_id}, {"$push": {"locations": location}}
        )

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "nickname": self.nickname,
            "status": self.status,
            "locations": self.locations,
        }

    def __str__(self):
        return f"{self.device_id} ({self.type})"
