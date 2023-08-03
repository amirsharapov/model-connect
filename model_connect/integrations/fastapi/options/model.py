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

    @classmethod
    @property
    def integration_name(cls) -> str:
        return 'fastapi'

    def resolve(self, connect_options: ConnectOptions):
        self._connect_options = connect_options

        self.resource_path = coalesce(
            self.resource_path,
            self._connect_options.model.name_plural_kebab_case,
        )

        self.resource_version = coalesce(
            self.resource_version,
            1
        )
