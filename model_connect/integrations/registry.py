from typing import Generator, TypeVar

from model_connect.integrations.base import (
    BaseIntegrationModel,
    BaseIntegrationModelField,
)

_ModelT = TypeVar(
    '_ModelT',
    bound=BaseIntegrationModel
)

_ModelFieldT = TypeVar(
    '_ModelFieldT',
    bound=BaseIntegrationModelField
)

_registry: dict[
    str,
    tuple[
        type[_ModelT],
        type[_ModelFieldT]
    ]
] = {}


def add(name: str, model: type[_ModelT], model_field: type[_ModelFieldT]):
    _registry[name] = (model, model_field)


def get(name: str) -> tuple[type[_ModelT], type[_ModelFieldT]]:
    return _registry[name]


def iterate() -> Generator[tuple[str, tuple[type[_ModelT], type[_ModelFieldT]]], None, None]:
    for name, (model, model_field) in _registry.items():
        yield name, (model, model_field)
