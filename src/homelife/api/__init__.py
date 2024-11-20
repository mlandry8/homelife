from flask import Flask

from homelife.container import Container
from homelife.api.views import device, server


app = Flask(__name__)
app.container = Container()
app.container.wire(
    modules=[
        "homelife.api.auth",
        "homelife.api.views.device",
        "homelife.api.views.server",
    ]
)

app.add_url_rule("/", "hello", lambda: "OK")

# Device URLS
app.add_url_rule(
    "/device/<device_id>", "initialise_device", device.post_device, methods=["POST"]
)
app.add_url_rule(
    "/device/<device_id>", "get_device", device.get_device, methods=["GET"]
)
app.add_url_rule(
    "/device/<device_id>/location",
    "post_location",
    device.post_location,
    methods=["POST"],
)

# Server URLS
app.add_url_rule("/server/devices", "get_devices", server.get_devices, methods=["GET"])

app.add_url_rule("/server/cert", "get_cert", server.get_cert, methods=["GET"])
