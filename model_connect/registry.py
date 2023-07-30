from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model_connect.connect import ConnectOptions

_registry = {}


def add(model_class: type, options: 'ConnectOptions'):
    _registry[model_class] = options


def get(model_class: type) -> 'ConnectOptions':
    return _registry[model_class]
