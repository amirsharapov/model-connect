from dataclasses import dataclass

from model_connect.adapters.psycopg2.config import Psycopg2Adapter
from model_connect.config.field import FieldConfig
from model_connect.config.fields import FieldsConfig
from model_connect.config.generic import GenericConfig
from model_connect.config.model_connect import ModelConnectConfig
from model_connect.adapters.fastapi.config import FastAPIAdapter
from model_connect.adapters.adapters import Adapters


class MissingFromDTO:
    pass


MISSING_FROM_DTO = MissingFromDTO()


@dataclass
class Person:
    __model_connect_config__ = ModelConnectConfig(
        fields=FieldsConfig(
            id=FieldConfig(
                is_identifier=True,
                adapters=Adapters(
                    FastAPIAdapter(
                        route_configs=GenericConfig(
                            name='id'
                        ),
                        dto_configs=GenericConfig(
                            include_in_post_request_dto=False,
                            include_in_get_response_dto=True,
                            default_value_if_not_in_request_dto=MISSING_FROM_DTO,
                        )
                    ),
                    Psycopg2Adapter(
                        is_sortable=True,
                        is_filterable=True
                    ),
                    CustomBusinessLogicAdapterConfig(
                        ...
                    ),
                    CustomProxyGeneratorAdapterConfig(
                        ...
                    )
                )
            )
        )
    )

    id: int
    name: str
    age: int


def custom_library_function(person: Person):
    # config = get_config()
    config = get_adapter_config(FastAPIAdapter)
