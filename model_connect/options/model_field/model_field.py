from dataclasses import Field, fields, dataclass, field
from types import NoneType
from typing import TYPE_CHECKING

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModelField, ModelFieldIntegrations
from model_connect.integrations import registry as integrations_registry
from model_connect.options.model_field.dtos.request import RequestDtos
from model_connect.options.model_field.dtos.response import ResponseDtos

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions


def has_default_value(dataclass_field: Field):
    return dataclass_field.default is not dataclass_field.default_factory


class ModelFields(dict[str, 'ModelField']):
    def resolve(
            self,
            options: 'ConnectOptions'
    ):
        # noinspection PyDataclass
        for dataclass_field in fields(options.dataclass_type):
            name = dataclass_field.name

            if name not in self:
                self[name] = ModelField()

            self[name].resolve(
                options,
                dataclass_field
            )


@dataclass
class ModelField:
    can_sort: bool = UNDEFINED
    can_filter: bool = UNDEFINED
    can_group: bool = UNDEFINED
    is_db_column: bool = UNDEFINED
    is_identifier: bool = UNDEFINED
    is_required_on_init: bool = UNDEFINED
    request_dtos: RequestDtos = UNDEFINED
    response_dtos: ResponseDtos = UNDEFINED
    query_params: tuple[str, ...] = UNDEFINED
    override_integrations: tuple['BaseIntegrationModelField', ...] = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    _dataclass_field: Field = field(
        init=False
    )

    _inferred_type: str = field(
        init=False
    )

    _name: str = field(
        init=False
    )

    _integrations: ModelFieldIntegrations = field(
        init=False,
        default_factory=dict
    )

    @property
    def dataclass_field(self):
        return self._dataclass_field

    @property
    def inferred_type(self):
        return self._inferred_type

    @property
    def name(self):
        return self._name

    @property
    def integrations(self):
        return self._integrations

    def resolve(
            self,
            connect_options: 'ConnectOptions',
            dataclass_field: Field
    ):
        self._inferred_type = dataclass_field.type
        self._name = dataclass_field.name

        if hasattr(self._inferred_type, '__args__'):
            type_args = self._inferred_type.__args__

            if len(type_args) == 2 and NoneType in type_args:
                self._inferred_type = coalesce(*type_args)

        self._connect_options = connect_options
        self._dataclass_field = dataclass_field

        self.can_sort = coalesce(
            self.can_sort,
            True
        )

        self.can_filter = coalesce(
            self.can_filter,
            True
        )

        self.can_group = coalesce(
            self.can_group,
            True
        )

        self.is_db_column = coalesce(
            self.is_db_column,
            True
        )

        self.is_identifier = coalesce(
            self.is_identifier,
            False
        )

        is_required_on_init = True

        if dataclass_field.init is False:
            is_required_on_init = False

        if has_default_value(dataclass_field):
            is_required_on_init = False

        self.is_required_on_init = coalesce(
            self.is_required_on_init,
            is_required_on_init
        )

        self.request_dtos = coalesce(
            self.request_dtos,
            RequestDtos()
        )

        self.response_dtos = coalesce(
            self.response_dtos,
            ResponseDtos()
        )

        self.override_integrations = coalesce(
            self.override_integrations,
            ()
        )

        self.request_dtos.resolve(connect_options, dataclass_field)
        self.response_dtos.resolve(connect_options, dataclass_field)

        for integration in self.override_integrations:
            name = integration.integration_name

            self._integrations[name] = integration
            self._integrations[name].resolve(connect_options, self)

        for name, _, model_field_class in integrations_registry.iterate():
            if name in self._integrations:
                continue

            model_field = model_field_class()
            model_field.resolve(connect_options, self)

            self._integrations[name] = model_field
