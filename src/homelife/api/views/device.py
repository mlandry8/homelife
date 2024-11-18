from flask import request
from dependency_injector.wiring import Provide, inject

from homelife.container import Container
from homelife.models.device import Device
from homelife.api.auth import authenticate

@inject
def post_device(device_id: str, device: Device=Provide[Container.models.device]):
    token = request.json.get("token")
    nickname = request.json.get("nickname")

    # attempt to initialise device
    # return 400 if token is already active or DNE
    try:
        device.intialise(token, device_id, nickname)
    except Exception as e:
        return {"message": str(e)}, 400

    return device.to_dict()

@authenticate()
@inject
def get_device(device_id: str, device: Device=Provide[Container.models.device]):
    device.retrieve(device_id=device_id)

    return device.to_dict()

@authenticate(device=True)
@inject
def post_location(device_id: str, device: Device=Provide[Container.models.device]):
    device.retrieve(device_id=device_id)

    # add location
    device.add_location(request.json)

    return device.to_dict()