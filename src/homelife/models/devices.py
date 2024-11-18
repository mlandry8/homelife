from homelife.models import Model

class Devices(Model):
    def __init__(self, db, collection):
        super().__init__(db, collection)

        self.devices = []

    def retrieve(self):
        self.devices = list(self.db.aggregate([
            {"$match": { "status": "active" }},
            {"$project": {
                "device_id": 1,
                "nickname": 1,
                "location": {"$arrayElemAt": ["$locations", -1]}
            }},
            {"$project": { "_id": 0 }}
        ]))
