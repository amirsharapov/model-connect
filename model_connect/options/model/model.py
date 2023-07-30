from typing import TypeVar

from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined
from model_connect.integrations.base import BaseIntegrationModel
from model_connect.integrations import registry as integrations_registry
from model_connect.options import ConnectOptions
from model_connect.options.model.query_params import QueryParams

_T = TypeVar('_T')


class Model(Base):
    def __init__(
            self,
            *,
            name_single: str = UNDEFINED,
            name_plural: str = UNDEFINED,
            query_params: 'QueryParams' = UNDEFINED,
            override_integrations: tuple['BaseIntegrationModel', ...] = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name_single = name_single
        self.name_plural = name_plural
        self.query_params = query_params
        self.override_integrations = override_integrations

        self._connect_options = None
        self._dataclass_type = None
        self._integrations = {}

    @property
    def connect_options(self) -> ConnectOptions:
        return self._connect_options

    @property
    def dataclass_type(self) -> _T:
        return self._dataclass_type

    @property
    def integrations(self) -> dict[type[_T], _T]:
        return self._integrations

    def resolve(self, options: ConnectOptions, dataclass_type: type):
        self._connect_options = options
        self._dataclass_type = dataclass_type

        self.name_single = (
            self.name_single
            if not is_undefined(self.name_single)
            else dataclass_type.__name__
        )

        self.name_plural = (
            self.name_plural
            if not is_undefined(self.name_plural)
            else None
        )

        self.query_params = (
            self.query_params
            if not is_undefined(self.query_params)
            else QueryParams()
        )

        self.override_integrations = (
            self.override_integrations
            if not is_undefined(self.override_integrations)
            else ()
        )

        self.query_params.resolve(options, dataclass_type)

        for integration in self.override_integrations:
            self._integrations[integration.__class__] = integration

        for integration_class, _ in integrations_registry.iterate():
            if integration_class in self._integrations:
                continue

            model_class = integration_class.model_class

            self._integrations[integration_class] = model_class()
            self._integrations[integration_class].resolve(options, dataclass_type)
