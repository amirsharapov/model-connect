from typing import TypeVar

from model_connect.constants import UNDEFINED
from model_connect.integrations.base import BaseIntegrationModel
from model_connect.options import ConnectOptions

_T = TypeVar('_T')


class Psycopg2Model(BaseIntegrationModel):
    def __init__(
            self,
            *,
            tablename: str = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.tablename = tablename

        self._connect_options = None

    def resolve(self, connect_options: ConnectOptions, dataclass_type: type):
        self._connect_options = connect_options

        self.tablename = (
            self.tablename
            if not self.tablename is UNDEFINED
            else dataclass_type.__name__.lower()
        )
