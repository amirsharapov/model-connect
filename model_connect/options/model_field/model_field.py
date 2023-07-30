from dataclasses import Field, fields, dataclass, field
from typing import TYPE_CHECKING

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModelField, ModelFieldIntegrations
from model_connect.integrations import registry as integrations_registry
from model_connect.options.model.query_params import QueryParams
from model_connect.options.model_field.model_field_dtos.request import RequestDtos
from model_connect.options.model_field.model_field_dtos.response import ResponseDtos

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions


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

            self[name].resolve(options, dataclass_field)


@dataclass
class ModelField:
    can_sort: bool = UNDEFINED
    can_filter: bool = UNDEFINED
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

    _type: type = field(
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
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    @property
    def integrations(self):
        return self._integrations

    def resolve(
            self,
            options: 'ConnectOptions',
            dataclass_field: Field
    ):
        self._type = dataclass_field.type
        self._name = dataclass_field.name

        self._connect_options = options
        self._dataclass_field = dataclass_field

        self.can_sort = coalesce(
            self.can_sort,
            True
        )

        self.can_filter = coalesce(
            self.can_filter,
            True
        )

        self.request_dtos = coalesce(
            self.request_dtos,
            RequestDtos()
        )

        self.response_dtos = coalesce(
            self.response_dtos,
            ResponseDtos()
        )

        self.query_params = coalesce(
            self.query_params,
            QueryParams()
        )

        self.override_integrations = coalesce(
            self.override_integrations,
            ()
        )

        self.request_dtos.resolve(options, dataclass_field)
        self.response_dtos.resolve(options, dataclass_field)

        for integration in self.override_integrations:
            self._integrations[integration.__class__] = integration

        for integration_class, _ in integrations_registry.iterate():
            model_field_class = integration_class.model_field_class

            if model_field_class not in self._integrations:
                self._integrations[model_field_class] = model_field_class()

            self._integrations[model_field_class].resolve(options, self)
