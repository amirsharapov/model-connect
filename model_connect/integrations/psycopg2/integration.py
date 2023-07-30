from model_connect.integrations.base import BaseIntegration


class Psycopg2Integration(BaseIntegration):
    model_class = None
    model_field_class = None
