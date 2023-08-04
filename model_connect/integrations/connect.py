from model_connect.integrations import type_registry
from model_connect.integrations.types import _ModelT, _ModelFieldT


def connect_integration(
        name: str,
        model_class: type[_ModelT],
        model_field_class: type[_ModelFieldT]
):
    type_registry.add(
        name,
        model_class,
        model_field_class
    )
