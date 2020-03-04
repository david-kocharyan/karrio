"""PurplShip Freight Gateway modules."""

import attr
from enum import Enum
from typing import Callable, Union
from purplship.core import Settings
from purplship.freight.proxy import Proxy
from purplship.freight.mapper import Mapper

import purplship.freight.mappers.dhl
import purplship.freight.mappers.fedex
import purplship.freight.mappers.ups


class Providers(Enum):
    dhl = purplship.freight.mappers.dhl
    fedex = purplship.freight.mappers.fedex
    ups = purplship.freight.mappers.ups


@attr.s(auto_attribs=True)
class Gateway:
    mapper: Mapper
    proxy: Proxy
    settings: Settings


@attr.s(auto_attribs=True)
class GatewayInitializer:
    initializer: Callable[[Union[Settings, dict]], Gateway]

    def create(self, settings: dict) -> Gateway:
        return self.initializer(settings)


class ProviderMapper:
    def __getitem__(self, key) -> GatewayInitializer:
        def initializer(settings: Union[Settings, dict]) -> Gateway:
            try:
                provider = Providers[key].value
                settings: provider.Settings = provider.Settings(**settings) if isinstance(settings, dict) else settings
                return Gateway(
                    settings=settings,
                    proxy=provider.Proxy(settings),
                    mapper=provider.Mapper(settings)
                )
            except KeyError as e:
                raise Exception(f"Unknown provider id '{key}'") from e

        return GatewayInitializer(initializer)


gateway = ProviderMapper()
