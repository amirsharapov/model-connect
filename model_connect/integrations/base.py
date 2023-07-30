from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar, Generic

if TYPE_CHECKING:
    from model_connect.options import ConnectOptions, ModelField

_T = TypeVar('_T')


class BaseIntegration:
    model_class: type['BaseIntegrationModel'] = None
    model_field_class: type['BaseIntegrationModelField'] = None


@dataclass
class BaseIntegrationModel(ABC):
    @abstractmethod
    def resolve(self, options: 'ConnectOptions'):
        ...


@dataclass
class BaseIntegrationModelField(ABC):
    @abstractmethod
    def resolve(self, options: 'ConnectOptions', model_field: 'ModelField'):
        ...


class ModelIntegrations(dict[type[_T], _T]):
    pass


class ModelFieldIntegrations(dict[type[_T], _T]):
    pass
