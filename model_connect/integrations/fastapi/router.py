from fastapi import APIRouter

from model_connect import registry
from model_connect.integrations.fastapi import FastAPIModel


def create_router(
        dataclass_type: type,
        add_prefix: bool = True,
        add_tags: bool = True
):
    options = registry.get(dataclass_type)
    options = options.model.integrations.get(FastAPIModel)

    return APIRouter(
        prefix=options.resource_path if add_prefix else '',
        tags=[options.tag_name] if add_tags else []
    )
