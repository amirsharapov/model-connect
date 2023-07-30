from model_connect.integrations.base import BaseIntegration
from model_connect.integrations.fastapi.options.model import FastAPIModel
from model_connect.integrations.fastapi.options.model_field import FastAPIModelField


class FastAPIIntegration(BaseIntegration):
    model_class = FastAPIModel
    model_field_class = FastAPIModelField
