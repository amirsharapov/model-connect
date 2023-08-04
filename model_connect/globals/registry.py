from typing import Optional, overload, Literal

from model_connect.globals.options.connect import GlobalConnectOptions
from model_connect.globals.options.fastapi import FastAPIGlobalOptions
from model_connect.globals.options.psycopg2 import Psycopg2GlobalOptions

_registry: dict[str, Optional[GlobalConnectOptions]] = {
    'global': None
}


@overload
def get(integration_name: None) -> GlobalConnectOptions:
    ...


@overload
def get(integration_name: Literal['psycopg2']) -> Psycopg2GlobalOptions:
    ...


@overload
def get(integration_name: Literal['fastapi']) -> FastAPIGlobalOptions:
    ...


def get(integration_name: str = None):
    options = _registry['global']

    if not options:
        raise Exception('Global options not set')

    if integration_name:
        options = options.integrations.get(
            integration_name
        )

    return options


def add(options):
    _registry['global'] = options
