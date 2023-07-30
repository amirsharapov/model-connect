from dataclasses import Field, fields
from typing import Callable, Any

from model_connect.base import Base
from model_connect.constants import is_undefined, UNDEFINED, iter_http_methods
from model_connect.integrations.base import BaseFieldOptions
from model_connect.options import ConnectOptions


class RequestDtos(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtos = {}

    def resolve(self, options: ConnectOptions, dataclass_type: type, dataclass_field: Field):
        pass


class RequestDtoOptions(Base):
    def __init__(
            self,
            *,
            include: bool = UNDEFINED,
            require: bool = UNDEFINED,
            preprocessor: Callable[[Any], Any] = UNDEFINED,
    ):
        super().__init__()
        self.include = include
        self.require = require
        self.preprocessor = preprocessor

        self._connect_options = None
        self._dataclass_type = None
        self._dataclass_field = None

    def resolve(
            self,
            options: ConnectOptions,
            dataclass_type: type,
            dataclass_field: Field
    ):
        self._connect_options = options
        self._dataclass_type = dataclass_type
        self._dataclass_field = dataclass_field

        self.include = (
            self.include
            if not is_undefined(self.include)
            else True
        )

        self.require = (
            self.require
            if not is_undefined(self.require)
            else False
        )

        self.preprocessor = (
            self.preprocessor
            if not is_undefined(self.preprocessor)
            else None
        )


class ResponseDtos(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtos = {}

    def resolve(self, options: ConnectOptions, dataclass_type: type, dataclass_field: Field):
        for method in iter_http_methods():
            if method not in self.dtos:
                self.dtos[method] = ResponseDtoOptions()

        for name, dto in self.dtos.items():
            self.dtos[name] = (
                dto
                if isinstance(dto, ResponseDtoOptions)
                else ResponseDtoOptions(**dto)
                if isinstance(dto, dict)
                else ResponseDtoOptions()
            )

            self.dtos[name].resolve(
                options,
                dataclass_type,
                dataclass_field
            )


class ResponseDtoOptions(Base):
    def __init__(
            self,
            *,
            include: bool = UNDEFINED,
            preprocessor: Callable[[Any], Any] = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.include = include
        self.preprocessor = preprocessor

        self._connect_options = None
        self._dataclass_type = None
        self._dataclass_field = None

    def resolve(self, options: ConnectOptions, dataclass_type: type, dataclass_field: Field):
        self._connect_options = options
        self._dataclass_type = dataclass_type
        self._dataclass_field = dataclass_field

        self.include = (
            self.include
            if not is_undefined(self.include)
            else True
        )

        self.preprocessor = (
            self.preprocessor
            if not is_undefined(self.preprocessor)
            else None
        )


class ModelFields(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = {}

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

            self.fields[name].resolve(options, dataclass_type)


class ModelField(Base):
    def __init__(
            self,
            *,
            can_sort: bool = UNDEFINED,
            can_filter: bool = UNDEFINED,
            request_dtos: dict[str, dict] = UNDEFINED,
            response_dtos: dict[str, dict] = UNDEFINED,
            query_params: tuple[str, ...] = UNDEFINED,
            custom_overrides: BaseFieldOptions | tuple['BaseFieldOptions', ...] = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self._type = UNDEFINED

        self.can_sort = can_sort
        self.can_filter = can_filter
        self.request_dtos = request_dtos
        self.response_dtos = response_dtos
        self.query_params = query_params

        self.custom_overrides = {}

        self._connect_options = None
        self._dataclass_type = None
        self._dataclass_field = None

        for override in custom_overrides:
            override_class = override.__class__
            self.custom_overrides[override_class] = override

    def resolve(
            self,
            options: ConnectOptions,
            dataclass_type: type,
            dataclass_field: Field
    ):
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
