from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined
from model_connect.options import ConnectOptions


class QueryParams(Base):
    def __init__(
            self,
            *,
            enable_count_flag: bool = UNDEFINED,
            enable_pagination: bool = UNDEFINED,
            enable_filtering: bool = UNDEFINED,
            enable_sorting: bool = UNDEFINED,
            pagination_limit_label: str = UNDEFINED,
            pagination_offset_label: str = UNDEFINED,
            count_flag_label: str = UNDEFINED,
            **kwargs
    ):
        super().__init__(**kwargs)
        self.enable_count = enable_count_flag
        self.enable_pagination = enable_pagination
        self.enable_filtering = enable_filtering
        self.enable_sorting = enable_sorting

        self.pagination_limit_label = pagination_limit_label
        self.pagination_offset_label = pagination_offset_label
        self.count_flag_label = count_flag_label

        self._connect_options = None
        self._dataclass_type = None

    def resolve(self, options: ConnectOptions, dataclass_type: type):
        self._connect_options = options
        self._dataclass_type = dataclass_type

        self.enable_count = (
            self.enable_count
            if not is_undefined(self.enable_count)
            else True
        )

        self.enable_pagination = (
            self.enable_pagination
            if not is_undefined(self.enable_pagination)
            else True
        )

        self.enable_filtering = (
            self.enable_filtering
            if not is_undefined(self.enable_filtering)
            else True
        )

        self.enable_sorting = (
            self.enable_sorting
            if not is_undefined(self.enable_sorting)
            else True
        )

        self.pagination_limit_label = (
            self.pagination_limit_label
            if not is_undefined(self.pagination_limit_label)
            else '$limit'
        )

        self.pagination_offset_label = (
            self.pagination_offset_label
            if not is_undefined(self.pagination_offset_label)
            else '$offset'
        )

        self.count_flag_label = (
            self.count_flag_label
            if not is_undefined(self.count_flag_label)
            else '$count'
        )
