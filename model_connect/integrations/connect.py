from model_connect.integrations.base import BaseIntegration
from model_connect.integrations import registry


def connect_integrations(*integrations: 'BaseIntegration'):
    for integration in integrations:
        assert isinstance(integration, BaseIntegration)
        assert isinstance(integration.model_class, type)
        assert isinstance(integration.model_field_class, type)

        #TODO: resolve integration options?

        registry.add(integration)
