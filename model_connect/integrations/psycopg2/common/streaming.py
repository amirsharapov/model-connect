from functools import cache
from typing import Iterator, TypeVar, Generator

from psycopg2.extras import DictCursor

from model_connect import registry
from model_connect.constants import UNDEFINED

_T = TypeVar("_T")


@cache
def get_required_field_names(dataclass_type: type[_T]):
    result = []

    for field in registry.get(dataclass_type).model_fields.values():
        if field.is_required_on_init:
            result.append(field.name)

    return result


def stream_from_cursor(cursor: DictCursor, max_chunk_size: int = 1000) -> Generator[dict, None, None]:
    while True:
        results = cursor.fetchmany(max_chunk_size)

        if not results:
            break

        for result in results:
            yield result


def stream_results_to_dataclass(results: Iterator[dict], dataclass_type: type[_T]) -> Generator[_T, None, None]:
    required_field_names = get_required_field_names(dataclass_type)

    for result in results:
        for field_name in required_field_names:
            if field_name not in result:
                result[field_name] = UNDEFINED

        yield dataclass_type(**result)
