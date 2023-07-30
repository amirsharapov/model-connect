from typing import TYPE_CHECKING, TypeVar

from model_connect.options import Model, ModelField

if TYPE_CHECKING:
    from model_connect.connect import ConnectOptions

_registry = {}
_T = TypeVar('_T')


def add(dataclass_type: type, options: 'ConnectOptions'):
    _registry[dataclass_type] = options


def get(dataclass_type: type) -> 'ConnectOptions':
    return _registry[dataclass_type]


def get_model(dataclass_type: type) -> 'Model':
    return get(dataclass_type).model


def get_model_field(dataclass_type: type, field_name: str) -> 'ModelField':
    return get(dataclass_type).model_fields.fields[field_name]


def get_model_integration(dataclass_type: type, integration_class: type[_T]) -> _T:
    return get(dataclass_type).model.integrations.get(integration_class)


def get_model_field_integration(dataclass_type: type, field_name: str, integration_class: type[_T]) -> _T:
    return get_model_field(dataclass_type, field_name).integrations.get(integration_class)
