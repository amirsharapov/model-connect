from dataclasses import is_dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model_connect.connect import ModelConnect

_registry = {}


def get_options(model_class) -> 'ModelConnect':
    if model_class not in _registry:
        _registry[model_class] = process_model(model_class)

    return _registry[model_class]


def process_model(model_class) -> 'ModelConnect':
    assert is_dataclass(model_class)

    config = getattr(
        model_class,
        '__model_connect_config__',
        None
    )

    assert config is not None, f'No config found for {model_class}'

    return config
