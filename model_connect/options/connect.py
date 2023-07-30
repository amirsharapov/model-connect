from dataclasses import dataclass, field

from model_connect.constants import UNDEFINED, coalesce
from model_connect.options.model.model import Model
from model_connect.options.model_field.model_field import ModelFields


@dataclass
class ConnectOptions:
    model: Model = UNDEFINED
    model_fields: ModelFields = UNDEFINED

    _dataclass_type: type = field(
        init=False
    )

    @property
    def dataclass_type(self):
        return self._dataclass_type

    def resolve(self, dataclass_type: type):
        self._dataclass_type = dataclass_type

        self.model = coalesce(
            self.model,
            Model()
        )

        self.model_fields = coalesce(
            self.model_fields,
            ModelFields()
        )

        self.model.resolve(self)
        self.model_fields.resolve(self)
