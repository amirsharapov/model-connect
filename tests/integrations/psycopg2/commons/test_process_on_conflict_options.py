from dataclasses import dataclass
from unittest import TestCase

from model_connect import connect
from model_connect.integrations.psycopg2.common.processing import process_on_conflict_options
from model_connect.options import ConnectOptions, ModelFields, ModelField


@dataclass
class Person:
    id: int
    name: str
    age: int


connect_options = ConnectOptions(
    model_fields=ModelFields(
        id=ModelField(
            is_identifier=True
        )
    )
)

class Tests(TestCase):
    def test_do_nothing(self):
        connect(Person, connect_options)

        processed_options = process_on_conflict_options(
            dataclass_type=Person,
            on_conflict_options={'do': 'nothing'}
        )

        self.assertEqual('NOTHING', processed_options.do)
        self.assertEqual(('id',), processed_options.conflict_targets)
        self.assertEqual((), processed_options.update_columns)

    def test_do_update(self):
        connect(Person, connect_options)

        processed_options = process_on_conflict_options(
            dataclass_type=Person,
            on_conflict_options={'do': 'update'}
        )

        self.assertEqual('UPDATE', processed_options.do)
        self.assertEqual(('id',), processed_options.conflict_targets)
        self.assertEqual(('name', 'age'), processed_options.update_columns)
