from model_connect.base import Base


class ModelConnect(Base):
    def __init__(
            self,
            model: 'Model' = None,
            fields: 'Fields' = None,
            *args,
            **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.model = model
        self.fields = fields


class Fields(Base): pass


class Field(Base): pass


class Model(Base): pass
