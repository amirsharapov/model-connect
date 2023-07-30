from dataclasses import Field
from typing import Callable, Any

from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined, iter_http_methods
from model_connect.options import ConnectOptions


class RequestDtos(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dtos = {}

    def resolve(
            self,
            options: ConnectOptions,
            dataclass_type: type,
            dataclass_field: Field
    ):
        for method in iter_http_methods():
            if method not in self.dtos:
                self.dtos[method] = RequestDto()

        for name, dto in self.dtos.items():
            self.dtos[name] = (
                dto
                if isinstance(dto, RequestDto)
                else RequestDto(**dto)
                if isinstance(dto, dict)
                else RequestDto()
            )

            self.dtos[name].resolve(
                options,
                dataclass_type,
                dataclass_field
            )


class RequestDto(Base):
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
