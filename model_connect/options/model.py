from typing import TypeVar

from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined
from model_connect.integrations.base import BaseModelOptions
from model_connect.options import ConnectOptions

_T = TypeVar('_T')


class Model(Base):
    def __init__(
            self,
            *,
            name_single: str = UNDEFINED,
            name_plural: str = UNDEFINED,
            sort_key: str = UNDEFINED,
            custom_overrides: tuple['BaseModelOptions', ...] = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.name_single = name_single
        self.name_plural = name_plural
        self.sort_key = sort_key

        self._connect_options = None
        self._dataclass_type = None

        self.custom_overrides = {}

        for override in custom_overrides:
            override_class = override.__class__
            self.custom_overrides[override_class] = override

    @property
    def connect_options(self) -> ConnectOptions:
        return self._connect_options

    @property
    def dataclass_type(self) -> _T:
        return self._dataclass_type

    def resolve(self, options: ConnectOptions, dataclass_type: type):
        self._connect_options = options
        self._dataclass_type = dataclass_type

        self.name_single = (
            self.name_single
            if not is_undefined(self.name_single)
            else dataclass_type.__name__
        )

        self.name_plural = (
            self.name_plural
            if not is_undefined(self.name_plural)
            else None
        )


# TODO: Implement
class QueryParams(Base):
    def __init__(
            self,
            *,
            enable_count_flag: bool = UNDEFINED,
            enable_pagination: bool = UNDEFINED,
            enable_filtering: bool = UNDEFINED,
            enable_sorting: bool = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.enable_count = enable_count_flag
        self.enable_pagination = enable_pagination
        self.enable_filtering = enable_filtering
        self.enable_sorting = enable_sorting
