from model_connect.constants import UNDEFINED
from model_connect.integrations.base import BaseIntegrationModel
from model_connect.options import ConnectOptions


class FastAPIModel(BaseIntegrationModel):
    def __init__(
            self,
            *,
            resource_path: str = UNDEFINED,
            resource_version: int = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.resource_path = resource_path
        self.resource_version = resource_version

        self._connect_options = None

    def resolve(self, connect_options: ConnectOptions, dataclass_type: type):
        self._connect_options = connect_options

        self.resource_path = (
            self.resource_path
            if not self.resource_path is UNDEFINED
            else dataclass_type.__name__.lower()
        )

        self.resource_version = (
            self.resource_version
            if not self.resource_version is UNDEFINED
            else 1
        )
