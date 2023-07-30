from model_connect.base import Base
from model_connect.constants import UNDEFINED, is_undefined
from model_connect.options import ModelFields, Model


class ConnectOptions(Base):
    def __init__(
            self,
            *,
            model: 'Model' = UNDEFINED,
            model_fields: 'ModelFields' = UNDEFINED,
            **kwargs,
    ):
        super().__init__(**kwargs)
        self.model = model
        self.model_fields = model_fields

        self._dataclass_type = None

    @property
    def dataclass_type(self):
        return self._dataclass_type

    def resolve(self, dataclass_type: type):
        self._dataclass_type = dataclass_type

        self.model = (
            self.model
            if not is_undefined(self.model)
            else Model()
        )

        self.model_fields = (
            self.model_fields
            if not is_undefined(self.model_fields)
            else ModelFields()
        )

        self.model.resolve(self, dataclass_type)
        self.model_fields.resolve(self, dataclass_type)
