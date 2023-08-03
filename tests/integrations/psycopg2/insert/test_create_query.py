from dataclasses import dataclass
from typing import Optional
from unittest import TestCase

from model_connect import connect
from model_connect.integrations.psycopg2 import create_insert_query
from model_connect.options import ConnectOptions, ModelFields, ModelField


@dataclass
class Person:
    id: Optional[int]
    name: str
    age: int


connect(
    Person,
    ConnectOptions(
        model_fields=ModelFields(
            id=ModelField(
                is_identifier=True
            )
        )
    )
)


class Tests(TestCase):
    def test(self):
        data = [
            Person(None, 'bob', 12),
            Person(None, 'joe', 13),
            Person(None, 'jane', 14),
        ]

        sql = create_insert_query(
            Person,
            data
        )

        self.assertEqual(
            'INSERT INTO people ( name , age ) VALUES %s RETURNING *',
            sql.sql
        )

        self.assertEqual(
            [
                ('bob', 12),
                ('joe', 13),
                ('jane', 14),
            ],
            sql.vars
        )

    def test_specific_columns(self):
        data = [
            Person(None, 'bob', 12),
            Person(None, 'joe', 13),
            Person(None, 'jane', 14),
        ]

        sql = create_insert_query(
            Person,
            data,
            columns=['name']
        )

        self.assertEqual(
            'INSERT INTO people ( name ) VALUES %s RETURNING *',
            sql.sql
        )

        self.assertEqual(
            [
                ('bob',),
                ('joe',),
                ('jane',),
            ],
            sql.vars
        )

    def test_one_row(self):
        data = Person(None, 'bob', 12)

        sql = create_insert_query(
            Person,
            [data]
        )

        self.assertEqual(
            'INSERT INTO people ( name , age ) VALUES %s RETURNING *',
            sql.sql
        )

        self.assertEqual(
            [(
                'bob',
                12,
            )],
            sql.vars
        )

    def test_on_conflict_do_nothing(self):
        data = Person(None, 'bob', 12)

        sql = create_insert_query(
            Person,
            [data],
            on_conflict_options={'do': 'nothing'}
        )

        self.assertEqual(
            'INSERT INTO people ( name , age ) VALUES %s ON CONFLICT ( id ) DO NOTHING RETURNING *',
            sql.sql
        )

        self.assertEqual(
            [(
                'bob',
                12,
            )],
            sql.vars
        )

    def test_on_conflict_do_update(self):
        data = Person(None, 'bob', 12)

        sql = create_insert_query(
            Person,
            [data],
            on_conflict_options={'do': 'update'}
        )

        self.assertEqual(
            'INSERT INTO people ( name , age ) VALUES %s ON CONFLICT ( id ) DO UPDATE SET name = EXCLUDED.name , age = EXCLUDED.age RETURNING *',
            sql.sql
        )

        self.assertEqual(
            [(
                'bob',
                12,
            )],
            sql.vars
        )
