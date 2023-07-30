from typing import TypeVar

from model_connect import get_options
from model_connect.integrations.base import BaseModelOptions, BaseFieldOptions

_T = TypeVar('_T')


class Psycopg2Model(BaseModelOptions):
    def __init__(
            self,
            tablename: str = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.tablename = tablename


class Psycopg2FieldOptions(BaseFieldOptions):
    def __init__(
            self,
            *args,
            can_filter: bool = True,
            can_sort: bool = True,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.can_filter = can_filter
        self.can_sort = can_sort


def get_tablename(model_class: type[_T]) -> str:
    options = get_options(model_class)
    options.model.options.get(Psycopg2FieldOptions)
