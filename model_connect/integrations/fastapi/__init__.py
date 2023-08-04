from model_connect.integrations.fastapi.options.model import FastAPIModel
from model_connect.integrations.fastapi.options.model_field import FastAPIModelField

from model_connect.integrations import registry as _integrations_registry


_integrations_registry.add(
    'fastapi',
    FastAPIModel,
    FastAPIModelField
)
