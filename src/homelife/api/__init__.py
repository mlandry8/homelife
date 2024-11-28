from os import path

from fastapi import FastAPI, Response

from homelife.api.routes.devices import router as device_router

app: FastAPI = FastAPI()


@app.get("/", response_model=dict[str, str])
async def hello():
    return {"message": "OK"}


@app.get("/cert", response_model=bytes)
async def get_cert():
    with open(f"{path.curdir}/etc/cert.pem", "rb") as f:
        cert: bytes = f.read()

    return Response(cert, media_type="application/x-x509-ca-cert")


app.include_router(device_router)
