from dataclasses import Field, dataclass, field
from typing import Callable, Any, TYPE_CHECKING

from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined, iter_http_methods, coalesce

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions


class RequestDtos(dict[str, 'RequestDto']):
    def resolve(
            self,
            options: 'ConnectOptions',
            dataclass_field: Field
    ):
        for method in iter_http_methods():
            if method not in self:
                self[method] = RequestDto()

        for name, dto in self.items():
            self[name] = coalesce(
                dto,
                RequestDto()
            )

            self[name].resolve(
                options,
                dataclass_field
            )


@dataclass
class RequestDto(Base):
    include: bool = UNDEFINED
    require: bool = UNDEFINED
    preprocessor: Callable[[Any], Any] = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    _dataclass_field: Field = field(
        init=False
    )

    def resolve(
            self,
            options: 'ConnectOptions',
            dataclass_field: Field
    ):
        self._connect_options = options
        self._dataclass_field = dataclass_field

        self.include = coalesce(
            self.include,
            True
        )

        self.require = coalesce(
            self.require,
            False
        )

        self.preprocessor = coalesce(
            self.preprocessor,
            None
        )
