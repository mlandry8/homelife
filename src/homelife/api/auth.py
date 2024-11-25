from functools import wraps
from typing import Any, Callable

from dependency_injector.wiring import Provide
from flask import jsonify, request

from homelife.container import Application
from homelife.models.device import Device


def validate_bearer_token(
    token: str, device_id:str|None=None, device: Device = Provide[Application.models.device] # type: ignore
) -> bool:
    device.retrieve(token=token, device_id=device_id)
    device_match: bool = device_id == device.device_id if device_id else True

    return device.is_set() and device_match


def authenticate(device:bool=False) -> Callable[..., Callable[..., Any]]:
    def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(f)
        def decorated_function(*args: tuple[Any], **kwargs: dict[Any, Any]) -> Any:
            auth_header: str | None = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token: str = auth_header.split(" ")[1]
                device_id: Any | None = kwargs.get("device_id") if device else None
                if validate_bearer_token(token, device_id):
                    return f(*args, **kwargs)
            return jsonify({"message": "Invalid or missing token"}), 401

        return decorated_function

    return decorator
