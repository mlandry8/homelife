from dependency_injector.wiring import Provide, inject

from homelife.container import Container
from homelife.models.devices import Devices
from homelife.api.auth import authenticate

@authenticate()
@inject
def get_devices(devices: Devices=Provide[Container.models.devices]):
    devices.retrieve()

    return devices.devices
