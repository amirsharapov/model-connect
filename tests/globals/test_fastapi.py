from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.connect import connect_psycopg2_integration, connect_fastapi_integration
from model_connect.globals.connect import connect_global_options
from model_connect.globals.options.connect import GlobalConnectOptions
from model_connect.globals.options.fastapi import FastAPIGlobalOptions
from model_connect.integrations.fastapi import FastAPIModel
from model_connect.integrations.fastapi.router import get_router_prefix
from model_connect.options import ConnectOptions, Model


class Tests(TestCase):
    def test(self):
        connect_global_options(
            GlobalConnectOptions(
                fastapi=FastAPIGlobalOptions(
                    base_prefix='/api',
                )
            )
        )

        @dataclass
        class Person:
            id: int

        connect_psycopg2_integration()
        connect_fastapi_integration()
        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_plural_parts=('persons',),
                    override_integrations=(
                        FastAPIModel(
                            resource_version=1
                        ),
                    )
                )
            )
        )

        prefix = get_router_prefix(Person)

        self.assertEqual(
            '/api/v1/persons',
            prefix
        )
