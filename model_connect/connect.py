from dataclasses import is_dataclass

from model_connect import registry
from model_connect.integrations.psycopg2 import Psycopg2ModelField, Psycopg2Model
from model_connect.options.connect import ConnectOptions

from model_connect.integrations.fastapi import FastAPIModel, FastAPIModelField
from model_connect.integrations import type_registry


def connect(dataclass_type: type, options: ConnectOptions = None):
    assert is_dataclass(dataclass_type)

    if options is None:
        options = ConnectOptions()

    options.resolve(dataclass_type)

    registry.add(
        dataclass_type,
        options
    )

    return dataclass_type


def connect_psycopg2_integration():
    type_registry.add(
        'psycopg2',
        Psycopg2Model,
        Psycopg2ModelField
    )


def connect_fastapi_integration():
    type_registry.add(
        'fastapi',
        FastAPIModel,
        FastAPIModelField
    )
