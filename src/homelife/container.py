from dependency_injector import containers
from dependency_injector.providers import (
    Configuration,
    Container,
    DependenciesContainer,
    Factory,
    Provider,
    Singleton,
)

from homelife.clients.mongo import MongoDBClient
from homelife.conf import conf
from homelife.models.device import Device
from homelife.models.devices import Devices


class Clients(containers.DeclarativeContainer):
    config: Configuration = Configuration()
    mongo_client: Provider[MongoDBClient] = Singleton(
        MongoDBClient,
        config.mongo.host,
        config.mongo.port,
        config.mongo.username,
        config.mongo.password,
        config.mongo.database,
    )


class Models(containers.DeclarativeContainer):
    config: Configuration = Configuration()
    clients: DependenciesContainer = DependenciesContainer()

    device: Factory[Device] = Factory(Device, clients.mongo_client, "devices")  # type: ignore
    devices: Factory[Devices] = Factory(Devices, clients.mongo_client, "devices")  # type: ignore


class Application(containers.DeclarativeContainer):
    config: Configuration = Configuration()
    config.from_dict(conf)

    clients: Container[Clients] = Container(Clients, config=config)
    models: Container[Models] = Container(Models, config=config, clients=clients)
