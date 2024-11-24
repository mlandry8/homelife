import secrets

from typing import Any, TYPE_CHECKING
from dependency_injector.wiring import Provide, inject

from homelife.utilities.crypto import get_certificate_fingerprint
from homelife.container import Application

if TYPE_CHECKING:
    from homelife.clients.mongo import MongoDBClient


@inject
def device_gen(
    mongo_client: MongoDBClient = Provide[Application.clients.mongo_client],  # type: ignore
) -> dict[str, str]:
    # Generate a secret token for the device
    token = secrets.token_urlsafe(32)
    mongo_client.collection("devices").insert_one({"token": token, "status": "pending"})

    server_info: dict[str, Any] | None = mongo_client.collection("server").find_one()

    if not server_info:
        raise Exception("Server info not found")

    invite_pkg: dict[str, str] = {
        "server": f'{server_info.get("ip")}:{server_info.get("port")}',
        "fingerprint": get_certificate_fingerprint(server_info.get("cert")),  # type: ignore
        "token": token,
    }

    print(invite_pkg)
    return invite_pkg


if __name__ == "__main__":
    container = Application()
    container.init_resources()  # type: ignore
    container.wire(modules=[__name__])

    device_gen()
