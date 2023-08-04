from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.connect import connect_psycopg2_integration, connect_fastapi_integration
from model_connect.globals.connect import connect_global_options
from model_connect.globals.options.connect import GlobalConnectOptions
from model_connect.globals.options.fastapi import FastAPIGlobalOptions
from model_connect.integrations.fastapi.router import get_router_prefix


class Tests(TestCase):
    def test(self):
        connect_global_options(
            GlobalConnectOptions(
                fastapi=FastAPIGlobalOptions(
                    base_prefix='/api',
                    default_resource_version=1
                )
            )
        )

        @dataclass
        class Person:
            id: int

        connect_psycopg2_integration()
        connect_fastapi_integration()
        connect(Person)

        prefix = get_router_prefix(Person)

        self.assertEqual(
            '/api/v1/people',
            prefix
        )
