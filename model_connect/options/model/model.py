import re
from dataclasses import dataclass, field
from typing import TypeVar, TYPE_CHECKING, Iterable

import inflect

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModel, ModelIntegrations
from model_connect.integrations import registry as integrations_registry
from model_connect.options.model.query_params import QueryParams

if TYPE_CHECKING:
    from model_connect.options.connect import ConnectOptions

_T = TypeVar('_T', bound=BaseIntegrationModel)

_inflect_engine = inflect.engine()


def split_model_name(name: str):
    return re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name)


def convert_name_parts_to_snake_case(name_parts: Iterable[str]):
    return '_'.join(name_parts).lower()


def convert_name_parts_to_kebab_case(name_parts: Iterable[str]):
    return '-'.join(name_parts).lower()


@dataclass
class Model:
    name_single_parts: Iterable[str] | str = UNDEFINED
    name_plural_parts: Iterable[str] | str = UNDEFINED
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

    @property
    def name_single_snake_case(self):
        return convert_name_parts_to_snake_case(self.name_single_parts)

    @property
    def name_plural_snake_case(self):
        return convert_name_parts_to_snake_case(self.name_plural_parts)

    @property
    def name_single_kebab_case(self):
        return convert_name_parts_to_kebab_case(self.name_single_parts)

    @property
    def name_plural_kebab_case(self):
        return convert_name_parts_to_kebab_case(self.name_plural_parts)

    def resolve(self, connect_options: 'ConnectOptions'):
        self._connect_options = connect_options

        self.name_single_parts = coalesce(
            self.name_single_parts,
            split_model_name(connect_options.dataclass_type.__name__)
        )

        name_single = ''.join(self.name_single_parts)
        name_plural = _inflect_engine.plural_noun(name_single)

        name_plural_parts = split_model_name(name_plural)

        self.name_plural_parts = coalesce(
            self.name_plural_parts,
            name_plural_parts
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
