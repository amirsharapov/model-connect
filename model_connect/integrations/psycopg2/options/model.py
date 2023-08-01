from dataclasses import dataclass, field
from typing import TypeVar, TYPE_CHECKING

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModel

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions

_T = TypeVar('_T')


@dataclass
class Psycopg2Model(BaseIntegrationModel):
    tablename: str = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    @classmethod
    @property
    def integration_name(cls) -> str:
        return 'psycopg2'

    def resolve(self, connect_options: 'ConnectOptions'):
        self._connect_options = connect_options

        self.tablename = coalesce(
            self.tablename,
            self._connect_options.model.name_plural,
            self._connect_options.model.name_single
        )

        self.tablename = self.tablename.lower()
