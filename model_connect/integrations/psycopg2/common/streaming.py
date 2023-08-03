from dataclasses import asdict
from functools import cache
from typing import Iterator, TypeVar, Generator, Iterable

from psycopg2.extras import DictCursor

from model_connect.constants import UNDEFINED
from model_connect.integrations.psycopg2 import Psycopg2ModelField
from model_connect.registry import get_model_fields

_T = TypeVar("_T")


class TuplesToInsert(list[tuple]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columns = None


@cache
def generate_insert_columns(dataclass_type: type[_T]) -> list[Psycopg2ModelField]:
    columns = []

    fields = get_model_fields(
        dataclass_type,
        'psycopg2'
    )

    for field in fields:
        if not field.include_in_insert:
            continue
        columns.append(field)

    return columns


def stream_from_cursor(cursor: DictCursor, max_chunk_size: int = 1000) -> Generator[dict, None, None]:
    while True:
        results = cursor.fetchmany(max_chunk_size)

        if not results:
            break

        for result in results:
            yield result


def stream_to_dataclass_type(results: Iterator[dict], dataclass_type: type[_T]) -> Generator[_T, None, None]:
    fields = get_model_fields(dataclass_type, 'psycopg2')
    fields = list(fields)

    for result in results:
        result = dict(result)
        for field in fields:
            if field.column_name not in result and field.model_field.is_required_on_init:
                result[field.column_name] = UNDEFINED
                continue

            if field.decoder:
                result[field.column_name] = field.decoder(
                    field,
                    result[field.column_name]
                )

        yield dataclass_type(**result)


def stream_dataclass_types_to_insert_tuples(
        dataclass_type: type[_T],
        data: Iterable[_T],
        columns: list[str]
) -> TuplesToInsert:
    fields = generate_insert_columns(dataclass_type)
    fields = [field for field in fields if field.column_name in columns]

    result = []

    for item in data:
        item_tuple = []

        if not isinstance(item, dict):
            item = asdict(item)

        for field in fields:
            if field.encoder:
                item[field.column_name] = field.encoder(
                    field,
                    item[field.column_name]
                )

            item_tuple.append(item[field.column_name])

        result.append(
            tuple(
                item[field.column_name] for
                field in
                fields
            )
        )

    result = TuplesToInsert(result)
    result.columns = columns

    return result
