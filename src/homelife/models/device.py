from pydantic import BaseModel

from homelife.models.location import Location


class Device(BaseModel):
    device_id: str | None = None
    token: str | None = None
    nickname: str | None = None
    status: str | None = None
    locations: list[Location] = []

    def is_set(self) -> bool:
        return all([self.device_id, self.token])


class PublicDevice(BaseModel):
    device_id: str | None = None
    nickname: str | None = None
    status: str | None = None
    locations: list[Location] = []


class PostDevice(BaseModel):
    device_id: str
    token: str
    nickname: str
