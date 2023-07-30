from .options import Psycopg2Model

class Psycopg2Integration(BaseIntegration):
    model_class = None
    model_field_class = None


connect_integrations(
    Psycopg2Integration()
)

