from typing import TYPE_CHECKING, TypeVar, overload


if TYPE_CHECKING:
    from model_connect.integrations.psycopg2 import Psycopg2Model, Psycopg2ModelField
    from model_connect.integrations.fastapi import FastAPIModel, FastAPIModelField
    from model_connect.options import Model, ModelField
    from model_connect.connect import ConnectOptions

_registry = {}
_IntegrationModelT = TypeVar('_IntegrationModelT', bound='BaseIntegrationModel')
_IntegrationModelFieldT = TypeVar('_IntegrationModelFieldT', bound='BaseIntegrationModelField')


def add(dataclass_type: type, options: 'ConnectOptions'):
    _registry[dataclass_type] = options


def get(dataclass_type: type) -> 'ConnectOptions':
    return _registry[dataclass_type]


def has(dataclass_type: type) -> bool:
    return dataclass_type in _registry


@overload
def get_model(
        dataclass_type: type,
        integration: str = 'psycopg2'
) -> 'Psycopg2Model':
    ...


@overload
def get_model(
        dataclass_type: type,
        integration: str = 'fastapi'
) -> 'FastAPIModel':
    ...


@overload
def get_model(
        dataclass_type: type,
        integration: str
) -> '_IntegrationModelT':
    ...


@overload
def get_model(
        dataclass_type: type,
        integration: None = None
) -> 'Model':
    ...


def get_model(
        dataclass_type: type,
        integration: str = None
):
    model = get(dataclass_type).model

    if integration is None:
        return model

    return model.integrations[integration]


@overload
def get_model_field(
        dataclass_type: type,
        field_name: str,
        integration: str = 'psycopg2'
) -> 'Psycopg2ModelField':
    ...


@overload
def get_model_field(
        dataclass_type: type,
        field_name: str,
        integration: str = 'fastapi'
) -> 'FastAPIModelField':
    ...


@overload
def get_model_field(
        dataclass_type: type,
        field_name: str,
        integration: str
) -> '_IntegrationModelFieldT':
    ...


@overload
def get_model_field(
        dataclass_type: type,
        field_name: str,
        integration: None = None
) -> 'ModelField':
    ...


def get_model_field(
        dataclass_type: type,
        field_name: str,
        integration: str = None
):
    model_fields = get(dataclass_type).model_fields
    model_field = model_fields.get(field_name)

    if integration is None:
        return model_field

    return model_field.integrations[integration]
