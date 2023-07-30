from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.integrations.psycopg2 import Psycopg2Model
from model_connect.integrations.psycopg2.select import create_select_query
from model_connect.options import ConnectOptions, Model


@dataclass
class Person:
    id: int
    name: str
    age: int


class Tests(TestCase):
    def test_filtering_invalid_column_names(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': 1,
                'blue': 'green',
                'name': {
                    '!=': 'John'
                }
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM person WHERE id = %s AND name != %s'
        )

        self.assertEqual(
            query.vars,
            [1, 'John']
        )

    def test_converting_eq_to_is(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': 1,
                'blue': 'green',
                'name': {
                    '=': None
                }
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM person WHERE id = %s AND name IS %s'
        )

    def test_converting_eq_to_in(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': [1, 2, 3],
                'blue': 'green',
                'name': {
                    '=': None
                }
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM person WHERE id IN %s AND name IS %s'
        )

        self.assertEqual(
            query.vars,
            [(1, 2, 3), None]
        )

    def test_name_plural(self):
        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_plural='people'
                )
            )
        )

        query = create_select_query(Person)

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM people'
        )

    def test_override(self):
        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_plural='people',
                    override_integrations=(
                        Psycopg2Model(
                            tablename='persons',
                        ),
                    )
                )
            )
        )

        query = create_select_query(Person)

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM persons'
        )

    def test_sorting(self):
        connect(
            Person,
            ConnectOptions(
                model=Model(
                    name_plural='people'
                )
            )
        )

        query = create_select_query(
            Person,
            sort_options={
                'id': 'asc',
                'name': 'desc'
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual(
            sql,
            'SELECT * FROM people ORDER BY id ASC, name DESC'
        )
