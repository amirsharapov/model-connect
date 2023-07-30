from dataclasses import Field, fields

from model_connect.base import Base
from model_connect.constants import is_undefined, UNDEFINED
from model_connect.integrations.base import BaseIntegrationModelField
from model_connect.integrations import registry as integrations_registry
from model_connect.options import ConnectOptions
from model_connect.options.model_field.model_field_dtos.request import RequestDtos
from model_connect.options.model_field.model_field_dtos.response import ResponseDtos


class ModelFields(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields: dict[str, ModelField] = {}

    def resolve(
            self,
            options: ConnectOptions,
            dataclass_type: type
    ):
        # noinspection PyDataclass
        for dataclass_field in fields(dataclass_type):
            name = dataclass_field.name

            if name not in self.fields:
                self.fields[name] = ModelField()

            self.fields[name].resolve(options, dataclass_type, dataclass_field)


class ModelField(Base):
    def __init__(
            self,
            *,
            can_sort: bool = UNDEFINED,
            can_filter: bool = UNDEFINED,
            request_dtos: dict[str, dict] = UNDEFINED,
            response_dtos: dict[str, dict] = UNDEFINED,
            query_params: tuple[str, ...] = UNDEFINED,
            override_integrations: tuple['BaseIntegrationModelField', ...] = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._type = None
        self._name = None

        self.can_sort = can_sort
        self.can_filter = can_filter
        self.request_dtos = request_dtos
        self.response_dtos = response_dtos
        self.query_params = query_params

        self.override_integrations = override_integrations

        self._integrations = {}
        self._connect_options = None
        self._dataclass_type = None
        self._dataclass_field = None

    @property
    def type(self):
        return self._type

    @property
    def name(self):
        return self._name

    def resolve(
            self,
            options: ConnectOptions,
            dataclass_type: type,
            dataclass_field: Field
    ):
        self._type = dataclass_field.type
        self._name = dataclass_field.name

        self._connect_options = options
        self._dataclass_type = dataclass_type
        self._dataclass_field = dataclass_field

        self.can_sort = (
            self.can_sort
            if not is_undefined(self.can_sort)
            else True
        )

        self.can_filter = (
            self.can_filter
            if not is_undefined(self.can_filter)
            else True
        )

        self.request_dtos = (
            self.request_dtos
            if not is_undefined(self.request_dtos)
            else RequestDtos(**self.request_dtos)
            if isinstance(self.request_dtos, dict)
            else RequestDtos()
        )

        self.response_dtos = (
            self.response_dtos
            if not is_undefined(self.response_dtos)
            else ResponseDtos(**self.response_dtos)
            if isinstance(self.response_dtos, dict)
            else ResponseDtos()
        )

        self.request_dtos.resolve(options, dataclass_type, dataclass_field)
        self.response_dtos.resolve(options, dataclass_type, dataclass_field)

        for integration in self.override_integrations:
            self._integrations[integration.__class__] = integration

        for integration_class, _ in integrations_registry.iterate():
            if integration_class in self._integrations:
                continue

            model_class = integration_class.model_class

            self._integrations[integration_class] = model_class()
            self._integrations[integration_class].resolve(options, dataclass_type)