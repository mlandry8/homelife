from fastapi import APIRouter, Depends, HTTPException, status

from homelife.api.verify import verify_token, verify_token_device_id
from homelife.models.device import Device, PostDevice, PublicDevice
from homelife.models.location import Location
from homelife.repositories.device import DeviceRepo

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


# get all devices w/ one location each
@router.get(
    "/",
    response_model=list[PublicDevice],
    dependencies=[Depends(verify_token)],
    status_code=status.HTTP_200_OK,
)
async def get_devices(
    device_repo: DeviceRepo,
):
    devices: list[PublicDevice] = [
        PublicDevice(**device.model_dump()) for device in device_repo.retrieve_many()
    ]
    return devices


# get single device w/ all locations TODO: add pagination
@router.get(
    "/{device_id}",
    response_model=PublicDevice,
    dependencies=[Depends(verify_token)],
    status_code=status.HTTP_200_OK,
)
async def get_device(
    device_id: str,
    device_repo: DeviceRepo,
):
    return PublicDevice(**device_repo.retrieve_one(device_id=device_id).model_dump())


# initiate device
@router.post("/", response_model=PublicDevice, status_code=status.HTTP_201_CREATED)
def post_device(
    device: PostDevice,
    device_repo: DeviceRepo,
):
    try:
        return PublicDevice(
            **device_repo.intialise(device).model_dump()
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# post a device location.
@router.post(
    "/{device_id}/location",
    response_model=PublicDevice,
    dependencies=[Depends(verify_token_device_id)],
    status_code=status.HTTP_201_CREATED,
)
def post_location(device_id: str, location: Location, device_repo: DeviceRepo):
    device: Device = device_repo.retrieve_one(device_id=device_id)
    device_repo.add_location(device, location)

    return PublicDevice(**device.model_dump())
