from dataclasses import dataclass
from unittest import TestCase

from model_connect.connect import connect
from model_connect.options import ConnectOptions, ModelField, ModelFields, Model
from model_connect.integrations.psycopg2 import Psycopg2Integration, Psycopg2Model
from model_connect.registry import get_model_options


class Tests(TestCase):
    def test(self):
        @dataclass
        class Person:
            name: str
            age: int

        connect(Person)

        tablename = get_model_options(Person).integrations.get(Psycopg2Model).tablename

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
                    )
                )
            )
        )

        tablename = get_model_options(Person).integrations.get(Psycopg2Model).tablename

        self.assertEqual(tablename, 'people')
