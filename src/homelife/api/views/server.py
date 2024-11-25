import os

from dependency_injector.wiring import Provide, inject
from typing import Any

from homelife.container import Application
from homelife.models.devices import Devices
from homelife.api.auth import authenticate


@authenticate()
@inject
def get_devices(devices: Devices = Provide[Application.models.devices] #type: ignore
        ) -> list[Any]:
    devices.retrieve()

    return devices.devices


def get_cert() -> bytes:
    with open(f"{os.path.curdir}/etc/cert.pem", "rb") as f:
        return f.read()
