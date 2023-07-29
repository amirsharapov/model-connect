from typing import TypeVar

from model_connect import get_options
from model_connect.connect import Field

_T = TypeVar('_T')


class Psycopg2ModelOptions(Field):
    def __init__(
            self,
            table_name: str = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.table_name = table_name


class Psycopg2FieldOptions(Field):
    def __init__(
            self,
            *args,
            can_filter_by: bool = True,
            can_sort_by: bool = True,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.can_filter_by = can_filter_by
        self.can_sort_by = can_sort_by


def get_tablename(model_class: type[_T]) -> str:
    options = get_options(model_class)
    return model_class._config.table_name
