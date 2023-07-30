from model_connect.integrations.base import BaseIntegration


def connect_integrations(*integrations: 'BaseIntegration'):
    for integration in integrations:
        assert isinstance(integration, BaseIntegration)
        assert isinstance(integration.model_class, type)
        assert isinstance(integration.model_field_class, type)
