from fastapi import APIRouter, FastAPI

from model_connect.registry import get_model


def attach_router(
        app: FastAPI,
        dataclass_type: type,
        router: APIRouter
):
    model = get_model(
        dataclass_type,
        'fastapi'
    )

    app.include_router(
        router,
        prefix=model.resource_path,
        tags=[model.tag_name]
    )
