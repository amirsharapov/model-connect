from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions, ModelField

_T = TypeVar('_T')


@dataclass
class BaseIntegrationModel(ABC):
    @classmethod
    @property
    @abstractmethod
    def integration_name(cls) -> str:
        ...

    @abstractmethod
    def resolve(self, options: 'ConnectOptions'):
        ...


@dataclass
class BaseIntegrationModelField(ABC):
    @classmethod
    @property
    @abstractmethod
    def integration_name(self) -> str:
        ...

    @abstractmethod
    def resolve(self, options: 'ConnectOptions', model_field: 'ModelField'):
        ...


class ModelIntegrations(dict[str, _T]):
    pass


class ModelFieldIntegrations(dict[str, _T]):
    pass
