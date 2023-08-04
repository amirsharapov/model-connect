from fastapi import APIRouter, FastAPI

from model_connect.registry import get_model
from model_connect.globals import registry as global_options


def get_router_prefix(dataclass_type: type):
    model = get_model(
        dataclass_type,
        'fastapi'
    )

    resource_path = global_options.get('fastapi').base_prefix
    resource_path = resource_path.rstrip('/')

    if model.resource_version is not None:
        resource_path = f'{resource_path}/v{model.resource_version}'

    if not model.resource_path.startswith('/'):
        resource_path += '/'

    resource_path = f'{resource_path}{model.resource_path}'

    return resource_path


def attach_router(
        app: FastAPI,
        dataclass_type: type,
        router: APIRouter
):
    model = get_model(
        dataclass_type,
        'fastapi'
    )

    resource_path = get_router_prefix(
        dataclass_type
    )

    app.include_router(
        router,
        prefix=resource_path,
        tags=[model.tag_name]
    )
