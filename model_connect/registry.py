from typing import TYPE_CHECKING, TypeVar, Optional

from model_connect.options import Model, ModelField

if TYPE_CHECKING:
    from model_connect.connect import ConnectOptions

_registry = {}
_T = TypeVar('_T')


def add(dataclass_type: type, options: 'ConnectOptions'):
    _registry[dataclass_type] = options


def get(dataclass_type: type) -> 'ConnectOptions':
    return _registry[dataclass_type]


def get_model_options(dataclass_type: type) -> 'Model':
    return get(dataclass_type).model


def get_model_field_options(dataclass_type: type, field_name: str) -> Optional['ModelField']:
    return get(dataclass_type).model_fields.get(field_name)
