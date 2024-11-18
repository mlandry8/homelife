from functools import wraps
from flask import request, jsonify
from dependency_injector.wiring import Provide, inject

from homelife.container import Container
from homelife.models.device import Device


def validate_bearer_token(token, device_id=None, device: Device=Provide[Container.models.device]): 
    device.retrieve(token=token, device_id=device_id)
    device_match = device_id == device.device_id if device_id else True

    return device.is_set() and device_match

def authenticate(device=False):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                device_id = kwargs.get('device_id') if device else None
                if validate_bearer_token(token, device_id):
                    return f(*args, **kwargs)
            return jsonify({"message": "Invalid or missing token"}), 401
        return decorated_function
    return decorator
