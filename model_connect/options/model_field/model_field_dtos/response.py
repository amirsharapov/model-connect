from dataclasses import Field, dataclass, field
from typing import Any, Callable, TYPE_CHECKING

from model_connect.constants import UNDEFINED, iter_http_methods, coalesce

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions


class ResponseDtos(dict[str, 'ResponseDto']):
    def resolve(
            self,
            connect_options: 'ConnectOptions',
            dataclass_field: Field
    ):
        for method in iter_http_methods():
            if method not in self:
                self[method] = ResponseDto()

        for name, dto in self.items():
            self[name] = coalesce(
                dto,
                ResponseDto()
            )

            self[name].resolve(
                connect_options,
                dataclass_field
            )


@dataclass
class ResponseDto:
    include: bool = UNDEFINED
    preprocessor: Callable[[Any], Any] = UNDEFINED

    _connect_options: 'ConnectOptions' = field(
        init=False
    )

    _dataclass_field: Field = field(
        init=False
    )

    def resolve(
            self,
            connect_options: 'ConnectOptions',
            dataclass_field: Field
    ):
        self._connect_options = connect_options
        self._dataclass_field = dataclass_field

        self.include = coalesce(
            self.include,
            True
        )

        self.preprocessor = coalesce(
            self.preprocessor,
            None
        )
