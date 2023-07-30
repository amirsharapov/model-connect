from typing import Generator, TypeVar

from model_connect.integrations.base import BaseIntegration

_T = TypeVar('_T', bound=BaseIntegration)
_registry: dict[type[_T], _T] = {}


def add(integration: _T):
    integration_class = integration.__class__
    _registry[integration_class] = integration


def get(integration_class: type[_T]) -> _T:
    return _registry[integration_class]


def iterate() -> Generator[tuple[type[_T], _T], None, None]:
    for key, value in _registry.items():
        yield key, value
