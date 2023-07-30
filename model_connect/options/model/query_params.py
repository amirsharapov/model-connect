from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from model_connect.constants import UNDEFINED, coalesce

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions


@dataclass
class QueryParams:
    enable_count: bool = UNDEFINED
    enable_pagination: bool = UNDEFINED
    enable_filtering: bool = UNDEFINED
    enable_sorting: bool = UNDEFINED

    pagination_limit_label: str = UNDEFINED
    pagination_offset_label: str = UNDEFINED
    count_flag_label: str = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    def resolve(self, connect_options: 'ConnectOptions'):
        self._connect_options = connect_options

        self.enable_count = coalesce(
            self.enable_count,
            True
        )
        self.enable_pagination = coalesce(
            self.enable_pagination,
            True
        )
        self.enable_filtering = coalesce(
            self.enable_filtering,
            True
        )
        self.enable_sorting = coalesce(
            self.enable_sorting,
            True
        )

        self.pagination_limit_label = coalesce(
            self.pagination_limit_label,
            '$limit'
        )
        self.pagination_offset_label = coalesce(
            self.pagination_offset_label,
            '$skip'
        )
        self.count_flag_label = coalesce(
            self.count_flag_label,
            '$count'
        )
