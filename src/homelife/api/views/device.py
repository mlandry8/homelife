from flask import request
from dependency_injector.wiring import Provide, inject
from typing import Literal, Any
from homelife.container import Application
from homelife.models.device import Device
from homelife.api.auth import authenticate


@inject
def post_device(
    device_id: str,
    device: Device = Provide[Application.models.device],  # type: ignore
) -> tuple[dict[str, str], Literal[400]] | dict[str, Any]:
    try:
        token: str = request.json.get("token")  # type: ignore
        nickname: str = request.json.get("nickname")  # type: ignore
    except AttributeError:
        return {"message": "Invalid request"}, 400

    # attempt to initialise device
    # return 400 if token is already active or DNE
    try:
        device.intialise(token, device_id, nickname)
    except Exception as e:
        return {"message": str(e)}, 400

    return device.to_dict()


@authenticate()
@inject
def get_device(
    device_id: str,
    device: Device = Provide[Application.models.device],  # type: ignore
) -> dict[str, Any]:
    device.retrieve(device_id=device_id)

    return device.to_dict()


@authenticate(device=True)
@inject
def post_location(
    device_id: str,
    device: Device = Provide[Application.models.device],  # type: ignore
) -> dict[str, Any]:
    device.retrieve(device_id=device_id)

    # add location
    device.add_location(request.json)

    return device.to_dict()
