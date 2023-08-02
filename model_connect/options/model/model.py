from dataclasses import dataclass, field
from typing import TypeVar, TYPE_CHECKING

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModel, ModelIntegrations
from model_connect.integrations import registry as integrations_registry
from model_connect.options.model.query_params import QueryParams

if TYPE_CHECKING:
    from model_connect.options.connect import ConnectOptions

_T = TypeVar('_T', bound=BaseIntegrationModel)


@dataclass
class Model:
    name_single: str = UNDEFINED
    name_plural: str = UNDEFINED
    query_params: 'QueryParams' = UNDEFINED
    override_integrations: tuple['BaseIntegrationModel', ...] = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    _integrations: ModelIntegrations = field(
        init=False,
        default_factory=dict
    )

    @property
    def integrations(self):
        return self._integrations

    def resolve(self, connect_options: 'ConnectOptions'):
        self._connect_options = connect_options

        self.name_single = coalesce(
            self.name_single,
            connect_options.dataclass_type.__name__
        )
        self.name_plural = coalesce(
            self.name_plural,
            None
        )
        self.query_params = coalesce(
            self.query_params,
            QueryParams()
        )
        self.override_integrations = coalesce(
            self.override_integrations,
            ()
        )

        self.query_params.resolve(connect_options)

        for integration in self.override_integrations:
            name = integration.integration_name

            self._integrations[name] = integration
            self._integrations[name].resolve(connect_options)

        for name, model_class, _ in integrations_registry.iterate():
            if name in self._integrations:
                continue

            model = model_class()
            model.resolve(connect_options)

            self._integrations[name] = model
