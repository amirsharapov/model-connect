from model_connect.integrations.psycopg2.options.model import Psycopg2Model
from model_connect.integrations.psycopg2.options.model_field import Psycopg2ModelField
from model_connect.integrations.psycopg2.select import (
    create_select_query,
    stream_select,
)
from model_connect.integrations.psycopg2.insert import (
    create_insert_query,
    stream_insert
)
from model_connect.integrations.psycopg2.update import (
    create_update_query,
    create_partial_update_query,
    stream_update,
    stream_partial_update
)
from model_connect.integrations.psycopg2.delete import (
    create_delete_query,
    stream_delete
)


from model_connect.integrations import registry as _integrations_registry

_integrations_registry.add(
    'psycopg2',
    Psycopg2Model,
    Psycopg2ModelField
)
