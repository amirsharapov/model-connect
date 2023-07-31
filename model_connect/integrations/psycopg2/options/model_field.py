from dataclasses import dataclass

from model_connect.constants import UNDEFINED, coalesce
from model_connect.integrations.base import BaseIntegrationModelField
from model_connect.options import ConnectOptions, ModelField


@dataclass
class Psycopg2ModelField(BaseIntegrationModelField):
    can_filter: bool = UNDEFINED
    can_sort: bool = UNDEFINED
    column_name: str = UNDEFINED
    include_in_insert: bool = UNDEFINED
    include_in_select: bool = UNDEFINED

    def resolve(self, options: 'ConnectOptions', model_field: 'ModelField'):
        self.can_filter = coalesce(
            self.can_filter,
            True
        )

        self.can_sort = coalesce(
            self.can_sort,
            True
        )

        self.column_name = coalesce(
            self.column_name,
            model_field.name
        )

        self.include_in_insert = coalesce(
            self.include_in_insert,
            not model_field.is_identifier
        )

        self.include_in_select = coalesce(
            self.include_in_select,
            True
        )
