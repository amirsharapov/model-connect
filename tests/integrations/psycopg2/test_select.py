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
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual('SELECT * FROM person WHERE id = %s', sql)
        self.assertEqual([1], query.vars)

    def test_converting_eq_to_is(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': 1,
                'name': {
                    '=': None,
                }
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual('SELECT * FROM person WHERE id = %s AND name IS %s', sql)
        self.assertEqual([1, None], query.vars)

    def test_like_operator(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': 1,
                'name': {
                    'like': '%o%',
                    '!=': [
                        'bob',
                        'joe'
                    ]
                }
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual('SELECT * FROM person WHERE id = %s AND name like %s AND name != %s AND name != %s', sql)
        self.assertEqual([1, '%o%', 'bob', 'joe'], query.vars)


    def test_converting_eq_to_in(self):
        connect(Person)

        query = create_select_query(
            Person,
            filter_options={
                'id': [1, 2, 3]
            }
        )

        sql = ' '.join(query.query.split())

        self.assertEqual('SELECT * FROM person WHERE id IN %s', sql)
        self.assertEqual([(1, 2, 3)], query.vars)

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

        self.assertEqual('SELECT * FROM people', sql)
        self.assertEqual([], query.vars)

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

        self.assertEqual('SELECT * FROM persons', sql)
        self.assertEqual([], query.vars)

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

        self.assertEqual('SELECT * FROM people ORDER BY id ASC, name DESC', sql)
        self.assertEqual([], query.vars)
