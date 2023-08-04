from typing import TypeVar

from model_connect.integrations.base import BaseIntegrationModelField, BaseIntegrationModel

_ModelT = TypeVar(
    '_ModelT',
    bound=BaseIntegrationModel
)

_ModelFieldT = TypeVar(
    '_ModelFieldT',
    bound=BaseIntegrationModelField
)