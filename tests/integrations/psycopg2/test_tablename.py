from dataclasses import dataclass
from unittest import TestCase

from model_connect.connect import ModelConnect, Model
from model_connect.integrations.fastapi.options import FastAPIModelOptions
from model_connect.integrations.psycopg2.options import get_tablename, Psycopg2ModelOptions


class Tests(TestCase):
    def test(self):

        @dataclass
        class Person:
            name: str
            age: int

        tablename = get_tablename(Person)

        self.assertEqual(tablename, 'person')

    def test_with_custom_tablename(self):

        @dataclass
        class Person:
            __model_connect__ = ModelConnect(
                model=Model(
                    integrations=(
                        Psycopg2ModelOptions(
                            tablename='people'
                        ),
                        FastAPIModelOptions(
                            route='/people'
                        )
                    )
                )
            )

            name: str
            age: int

        tablename = get_tablename(Person)

        self.assertEqual(tablename, 'people')
