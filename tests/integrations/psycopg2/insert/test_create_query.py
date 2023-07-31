from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.integrations.psycopg2 import create_insert_query
from model_connect.options import ConnectOptions, ModelFields, ModelField


@dataclass
class Person:
    id: int
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
            Person(1, 'bob', 12),
            Person(2, 'joe', 13),
            Person(3, 'jane', 14),
        ]

        sql = create_insert_query(
            Person,
            data
        )

        self.assertEqual(
            'INSERT INTO person ( name , age ) VALUES %s RETURNING *',
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
