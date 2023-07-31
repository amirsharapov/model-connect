from dataclasses import dataclass, field

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModel
from model_connect.options import ConnectOptions


@dataclass
class FastAPIModel(BaseIntegrationModel):
    resource_path: str = UNDEFINED
    resource_version: int = UNDEFINED
    tag_name: str = UNDEFINED

    _connect_options: ConnectOptions = field(
        init=False
    )

    def resolve(self, connect_options: ConnectOptions):
        self._connect_options = connect_options

        self.resource_path = coalesce(
            self.resource_path,
            self._connect_options.dataclass_type.__name__.lower()
        )

        self.resource_version = coalesce(
            self.resource_version,
            1
        )

        self.tag_name = coalesce(
            self.tag_name,
            self._connect_options.dataclass_type.__name__
        )
