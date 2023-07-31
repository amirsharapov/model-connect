from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.integrations.psycopg2.select import process_filter_options


@dataclass
class Person:
    id: int
    name: str
    age: int
    computers_owned: int


connect(Person)


class Tests(TestCase):
    def test(self):
        filter_options = {
            'name': {
                'LIKE': '%o%',
                '!=': ['joe', 'bob']
            },
            'id': [1, 2, 3],
            'computers_owned': {
                'IN': [1, 2]
            },
            'age': 12
        }
        vars_ = []

        actual = list(
            process_filter_options(
                Person,
                filter_options,
                vars_
            )
        )

        expected = [
            {'column': 'name', 'operator': 'LIKE', 'value': '%s'},
            {'column': 'name', 'operator': '!=', 'value': '%s'},
            {'column': 'name', 'operator': '!=', 'value': '%s'},
            {'column': 'id', 'operator': 'IN', 'value': '%s'},
            {'column': 'computers_owned', 'operator': 'IN', 'value': '%s'},
            {'column': 'age', 'operator': '=', 'value': '%s'}
        ]

        self.assertEqual(expected, actual)
        self.assertEqual(
            [
                '%o%',
                'joe',
                'bob',
                (1, 2, 3),
                (1, 2),
                12
            ],
            vars_
        )
