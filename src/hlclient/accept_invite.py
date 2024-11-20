import requests
import secrets

from hlclient import HOST, FINGER, TOKEN, NICKNAME
from homelife.utilities.crypto import verify_certificate_fingerprint


def accept_request(host, finger, token, nickname):
    # unverified tls connection
    cert = requests.get(f"https://{host}/server/cert", verify=False).content

    # verify cert
    if not verify_certificate_fingerprint(cert, finger):
        raise Exception("Invalid certificate")

    # init device with server
    device_id = secrets.token_urlsafe(32)
    requests.post(
        f"https://{host}/device/{device_id}",
        json={"token": token, "nickname": nickname},
        verify="etc/cert.pem",
    ).raise_for_status()

    # get device info
    device = requests.get(
        f"https://{host}/device/{device_id}",
        headers={"Authorization": f"Bearer {token}"},
        verify="etc/cert.pem",
    ).json()

    print(device)


if __name__ == "__main__":
    accept_request(HOST, FINGER, TOKEN, NICKNAME)
