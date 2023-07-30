from model_connect.integrations.base import BaseIntegration
from model_connect.integrations.connect import connect_integrations
from model_connect.integrations.psycopg2.options.model import Psycopg2Model
from model_connect.integrations.psycopg2.options.model_field import Psycopg2ModelField


class Psycopg2Integration(BaseIntegration):
    model_class = Psycopg2Model
    model_field_class = Psycopg2ModelField


connect_integrations(
    Psycopg2Integration()
)
