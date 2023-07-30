from typing import Generator

from model_connect.integrations.base import BaseIntegration

_registry: dict[type[BaseIntegration], BaseIntegration] = {}


def add(integration: BaseIntegration):
    integration_class = integration.__class__
    _registry[integration_class] = integration


def iterate() -> Generator[tuple[type[BaseIntegration], BaseIntegration], None, None]:
    for key, value in _registry.items():
        yield key, value
