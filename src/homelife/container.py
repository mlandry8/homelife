from dependency_injector import containers, providers
from dependency_injector.providers import Configuration, Container, Factory, DependenciesContainer, Provider

from homelife.clients.mongo import MongoDBClient
from homelife.conf import conf
from homelife.models.device import Device
from homelife.models.devices import Devices


class Clients(containers.DeclarativeContainer):
    config: Configuration = providers.Configuration()
    mongo_client: Provider[MongoDBClient] = providers.Singleton(
        MongoDBClient,
        config.mongo.host,
        config.mongo.port,
        config.mongo.username,
        config.mongo.password,
        config.mongo.database,
    )

class Models(containers.DeclarativeContainer):
    config: Configuration = providers.Configuration()
    clients: DependenciesContainer = providers.DependenciesContainer()

    device: Factory[Device] = providers.Factory(Device, clients.mongo_client, "devices")  # type: ignore
    devices: Factory[Devices] = providers.Factory(Devices, clients.mongo_client, "devices") # type: ignore


class Application(containers.DeclarativeContainer):
    config: Configuration = providers.Configuration()
    config.from_dict(conf)

    clients: Container[Clients] = providers.Container(Clients, config=config)
    models: Container[Models] = providers.Container(Models, config=config, clients=clients)
