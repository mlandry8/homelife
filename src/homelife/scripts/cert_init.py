import requests
import os

from dependency_injector.wiring import Provide, inject

from homelife.container import Container
from homelife.utilities.crypto import generate_cert


@inject
def cert_init(mongo_client=Provide[Container.clients.mongo_client]):
    external_ip = requests.get(
        "https://api.ipify.org",
        params={'format': 'json'}).json()['ip']

    server_info = mongo_client.collection('server').find_one()

    if server_info.get('ip') != external_ip:
        cert, private = generate_cert(external_ip)

        # get old thumbrint
        # register new thumbprint with discovery service
        # write new thumbprint

        mongo_client.collection('server').update_one(
            {'_id': 'server_info'},
            {'$set': {
                'ip': external_ip,
                'port': 5000,
                'cert': cert,
                'priv': private,
                'status': 'current'
            }},
            upsert=True
        )
        server_info = mongo_client.collection('server').find_one()

    with open(f'{os.path.curdir}/etc/cert.pem', 'wb') as f:
        f.write(server_info.get('cert'))

    with open(f'{os.path.curdir}/etc/key.pem', 'wb') as f:
        f.write(server_info.get('priv'))

if __name__ == '__main__':
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    cert_init()
