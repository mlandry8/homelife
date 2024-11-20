import secrets

from dependency_injector.wiring import Provide, inject

from homelife.utilities.crypto import get_certificate_fingerprint
from homelife.container import Container


@inject
def device_gen(mongo_client=Provide[Container.clients.mongo_client]):
    # Generate a secret token for the device
    token = secrets.token_urlsafe(32)
    mongo_client.collection("devices").insert_one({"token": token, "status": "pending"})

    server_info = mongo_client.collection("server").find_one()

    invite_pkg = {
        "server": f'{server_info.get("ip")}:{server_info.get("port")}',
        "fingerprint": get_certificate_fingerprint(server_info.get("cert")),
        "token": token,
    }

    print(invite_pkg)
    return invite_pkg


if __name__ == "__main__":
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    device_gen()
