from dataclasses import dataclass

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModelField
from model_connect.options import ConnectOptions, ModelField


@dataclass
class Psycopg2ModelField(BaseIntegrationModelField):
    can_filter: bool = UNDEFINED
    can_sort: bool = UNDEFINED

    def resolve(self, options: 'ConnectOptions', model_field: 'ModelField'):
        self.can_filter = coalesce(
            self.can_filter,
            True
        )

        self.can_sort = coalesce(
            self.can_sort,
            True
        )
