from fastapi import APIRouter

from model_connect.registry import get_model


def create_router(
        dataclass_type: type,
        add_prefix: bool = True,
        add_tags: bool = True
):
    options = get_model(dataclass_type, 'fastapi')

    return APIRouter(
        prefix=options.resource_path if add_prefix else '',
        tags=[options.tag_name] if add_tags else []
    )
