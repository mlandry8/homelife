from typing import Annotated

from fastapi import Header, HTTPException, status

from homelife.models.device import Device
from homelife.repositories.device import DeviceRepo


class VerifyToken:
    def __init__(self, match: bool = False) -> None:
        self.match: bool = match

    def __call__(
        self,
        Authorization: Annotated[str, Header()],
        device_repo: DeviceRepo,
        device_id: str | None = None,
    ) -> bool:
        if Authorization and Authorization.startswith("Bearer "):
            token: str = Authorization.split(" ")[1]
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing token",
            )

        try:
            if self.match:
                device: Device = device_repo.retrieve_one(
                    token=token, device_id=device_id, strict=True
                )

                return device.is_set() and device_id == device.device_id

            else:
                return device_repo.retrieve_one(token=token).is_set()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or unauthorized token",
            )


verify_token = VerifyToken()
verify_token_device_id = VerifyToken(match=True)
