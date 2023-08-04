from typing import Generator

from model_connect.integrations.types import _ModelT, _ModelFieldT


_registry: dict[
    str,
    tuple[
        type[_ModelT],
        type[_ModelFieldT]
    ]
] = {}


def add(name: str, model_class: type[_ModelT], model_field_class: type[_ModelFieldT]):
    _registry[name] = (model_class, model_field_class)


def get(name: str) -> tuple[type[_ModelT], type[_ModelFieldT]]:
    return _registry[name]


def iterate() -> Generator[tuple[str, type[_ModelT], type[_ModelFieldT]], None, None]:
    for name, (model_class, model_field_class) in _registry.items():
        yield name, model_class, model_field_class
