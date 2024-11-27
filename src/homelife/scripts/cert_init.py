import os
from typing import TYPE_CHECKING, Any

import requests

from homelife.clients.mongo import get_mongo_client
from homelife.utilities.crypto import generate_cert

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


def cert_init(mongo_client: "MongoDBClient") -> None:
    external_ip: str | None = requests.get(
        "https://api.ipify.org", params={"format": "json"}
    ).json()["ip"]

    server_info: dict[Any, Any] | None = mongo_client.collection("server").find_one()

    if not server_info or server_info.get("ip") != external_ip:
        cert: bytes
        private: bytes
        cert, private = generate_cert(external_ip)

        # TODO: register with discovery service

        mongo_client.collection("server").update_one(
            {"_id": "server_info"},
            {
                "$set": {
                    "ip": external_ip,
                    "port": 8000,
                    "cert": cert,
                    "priv": private,
                    "status": "current",
                }
            },
            upsert=True,
        )
        server_info = mongo_client.collection("server").find_one()

    try:
        with open(f"{os.path.curdir}/etc/cert.pem", "wb") as f:
            f.write(server_info.get("cert"))  # type: ignore

        with open(f"{os.path.curdir}/etc/key.pem", "wb") as f:
            f.write(server_info.get("priv"))  # type: ignore

    except (AttributeError, TypeError):
        raise Exception("Invalid server info")


if __name__ == "__main__":
    cert_init(get_mongo_client())
