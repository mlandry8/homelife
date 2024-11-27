from os import path

from fastapi import FastAPI

from homelife.api.routes.devices import router as device_router

app: FastAPI = FastAPI()


@app.get("/")
async def hello() -> dict[str, str]:
    return {"message": "OK"}


@app.get("/cert")
async def get_cert() -> bytes:
    with open(f"{path.curdir}/etc/cert.pem", "rb") as f:
        return f.read()


app.include_router(device_router)
