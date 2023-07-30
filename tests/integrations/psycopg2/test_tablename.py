from dataclasses import dataclass
from unittest import TestCase

from model_connect.connect import connect
from model_connect.options import ConnectOptions, ModelField, ModelFields, Model
from model_connect.integrations.connect import connect_integrations
from model_connect.integrations.psycopg2 import Psycopg2Integration
from model_connect.registry import get_model_integration


class Tests(TestCase):
    def test(self):

        @dataclass
        class Person:
            name: str
            age: int

        connect(Person)
        connect_integrations(
            Psycopg2Integration()
        )

        tablename = get_model_integration(Person, Psycopg2Integration).model_class.tablename

        self.assertEqual(tablename, 'person')

    def test_with_custom_tablename(self):

        @dataclass
        class Person:
            name: str
            age: int
            username: str
            password: str

        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_single='person',
                    name_plural='people',
                ),
                model_fields=ModelFields(
                    password=ModelField(
                        can_filter=False,
                        can_sort=False,
                        request_dtos=dict(
                            defaults=dict(
                                preprocessor=lambda value: hash(value)
                            )
                        ),
                        response_dtos=dict(
                            defaults=dict(
                                exclude=True
                            )
                        )
                    )
                )
            )
        )

        connect_integrations(
            Psycopg2Integration()
        )

        tablename = get_tablename(Person)

        self.assertEqual(tablename, 'people')
