from model_connect.integrations.base import BaseIntegrationModelField
from model_connect.options import ConnectOptions, ModelField


class FastAPIModelField(BaseIntegrationModelField):
    @classmethod
    @property
    def integration_name(cls) -> str:
        return 'fastapi'

    def resolve(self, options: 'ConnectOptions', model_field: 'ModelField'):
        pass
