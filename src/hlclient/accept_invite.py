import secrets

import requests

from hlclient import FINGER, HOST, NICKNAME, TOKEN
from homelife.utilities.crypto import verify_certificate_fingerprint


def accept_request(host: str, finger: str, token: str, nickname: str) -> None:
    # unverified tls connection
    cert: bytes = requests.get(f"https://{host}/server/cert", verify=False).content

    # verify cert
    if not verify_certificate_fingerprint(cert, finger):
        raise Exception("Invalid certificate")

    # init device with server
    device_id: str = secrets.token_urlsafe(32)
    requests.post(
        f"https://{host}/device/{device_id}",
        json={"token": token, "nickname": nickname},
        verify="etc/cert.pem",
    ).raise_for_status()

    # get device info
    device: dict[str, str] = requests.get(
        f"https://{host}/device/{device_id}",
        headers={"Authorization": f"Bearer {token}"},
        verify="etc/cert.pem",
    ).json()

    print(device)


if __name__ == "__main__":
    accept_request(HOST, FINGER, TOKEN, NICKNAME)
