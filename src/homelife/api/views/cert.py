import os

def get_cert():
    with open(f"{os.path.curdir}/etc/cert.pem", "rb") as f:
        return f.read()