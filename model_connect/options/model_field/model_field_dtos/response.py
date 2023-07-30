from dataclasses import Field
from typing import Any, Callable

from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined, iter_http_methods
from model_connect.options import ConnectOptions


class ResponseDtos(Base):
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
                self.dtos[method] = ResponseDto()

        for name, dto in self.dtos.items():
            self.dtos[name] = (
                dto
                if isinstance(dto, ResponseDto)
                else ResponseDto(**dto)
                if isinstance(dto, dict)
                else ResponseDto()
            )

            self.dtos[name].resolve(
                options,
                dataclass_type,
                dataclass_field
            )


class ResponseDto(Base):
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
