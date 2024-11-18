from flask import Flask

from homelife.container import Container
from homelife.api.views import device, devices, cert


app = Flask(__name__)
app.container = Container()
app.container.wire(modules=[
    "homelife.api.auth",
    "homelife.api.views.device",
    "homelife.api.views.devices"])

app.add_url_rule("/", "hello",  lambda: "OK")

# Device URLS
app.add_url_rule(
    "/device/<device_id>", "initialise_device",
    device.post_device, methods=["POST"]
)
app.add_url_rule(
    "/device/<device_id>", "get_device",
    device.get_device, methods=["GET"]
)
app.add_url_rule(
    "/device/<device_id>/location", "post_location",
    device.post_location, methods=["POST"]
)

# Devices URLS
app.add_url_rule(
    "/devices", "get_devices",
    devices.get_devices, methods=["GET"]
)

# Cert URLS
app.add_url_rule(
    "/cert", "get_cert",
    cert.get_cert, methods=["GET"]
)




