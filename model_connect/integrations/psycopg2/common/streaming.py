from typing import Iterator, TypeVar, Generator

from psycopg2.extras import DictCursor

_T = TypeVar("_T")


def stream_from_cursor(cursor: DictCursor, max_chunk_size: int = 1000) -> Generator[dict, None, None]:
    while True:
        results = cursor.fetchmany(max_chunk_size)

        if not results:
            break

        for result in results:
            yield result


def stream_results_to_model_type(results: Iterator[dict], model_class: type[_T]) -> Generator[_T, None, None]:
    for result in results:
        yield model_class(**result)
