from dependency_injector import containers, providers

from homelife.conf import conf
from homelife.clients.mongo import MongoDBClient
from homelife.models.device import Device
from homelife.models.devices import Devices


class Models(containers.DeclarativeContainer):
    config = providers.Configuration()
    clients = providers.DependenciesContainer()

    device = providers.Factory(
        Device,
        clients.mongo_client, 'devices'
    )
    devices = providers.Factory(
        Devices,
        clients.mongo_client, 'devices'
    )

class Clients(containers.DeclarativeContainer):
    config = providers.Configuration()
    mongo_client = providers.Singleton(
        MongoDBClient,
        config.mongo.host, config.mongo.port,
        config.mongo.username, config.mongo.password,
        config.mongo.database
    )

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    config.from_dict(conf)

    clients = providers.Container(
        Clients, config=config
    )
    models = providers.Container(
        Models,
        config=config,
        clients=clients
    )

