from model_connect.base import Base


class BaseIntegration(Base):
    model_class: 'BaseModelOptions' = None
    model_field_class: 'BaseFieldOptions' = None


class BaseModelOptions(Base): pass


class BaseFieldOptions(Base): pass
