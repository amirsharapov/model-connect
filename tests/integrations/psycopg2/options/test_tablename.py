from dataclasses import dataclass
from unittest import TestCase

from model_connect.connect import connect
from model_connect.options import ConnectOptions, ModelField, ModelFields, Model
from model_connect.integrations.psycopg2 import Psycopg2Model
from model_connect.registry import get_model


class Tests(TestCase):
    def test(self):
        @dataclass
        class Person:
            name: str
            age: int

        connect(Person)

        tablename = get_model(Person, 'psycopg2').tablename

        self.assertEqual(tablename, 'people')

    def test_with_custom_tablename(self):
        @dataclass
        class Person:
            name: str
            age: int

        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_plural_parts=('people',),
                )
            )
        )

        tablename = get_model(Person, 'psycopg2').tablename

        self.assertEqual(tablename, 'people')
