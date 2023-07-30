from model_connect.base import Base


class BaseIntegration(Base):
    model_class: type['BaseIntegrationModel'] = None
    model_field_class: type['BaseIntegrationModelField'] = None


class BaseIntegrationModel(Base): pass


class BaseIntegrationModelField(Base): pass
