from dataclasses import dataclass, field, asdict
from typing import Iterable, TypeVar, Generator

from jinja2 import Template
from psycopg2.extras import DictCursor, execute_values

from model_connect.integrations.psycopg2.common.processing import process_on_conflict_options
from model_connect.integrations.psycopg2.common.streaming import (
    stream_from_cursor,
    stream_to_dataclass_type,
    stream_dataclass_types_to_insert_tuples,
    generate_insert_columns
)
from model_connect.registry import get_model

_T = TypeVar('_T')


@dataclass
class InsertSQL:
    sql: str
    vars: list = field(
        default_factory=list
    )


def create_insert_query(
        dataclass_type: type[_T],
        data: Iterable[_T],
        columns: list[str] = None,
        on_conflict_options: dict = None
) -> InsertSQL:
    vars_ = []

    model = get_model(
        dataclass_type,
        'psycopg2'
    )

    if not columns:
        columns = generate_insert_columns(dataclass_type)
        columns = [column.column_name for column in columns]

    if on_conflict_options is not None:
        on_conflict_options = process_on_conflict_options(
            dataclass_type,
            on_conflict_options
        )

    values = stream_dataclass_types_to_insert_tuples(
        dataclass_type,
        data,
        columns
    )

    vars_.extend(values)

    template = Template('''
        INSERT INTO
            {{ tablename }}
            (
                {%- for column in columns %}
                {{ column }}
                {%- if not loop.last %}
                    ,
                {%- endif %}
                {%- endfor %}
            )
        VALUES
            %s
        
        {%- if on_conflict_options %}
            ON CONFLICT (
                {%- for column in on_conflict_options.conflict_targets %}
                {{ column }}
                {%- if not loop.last %}
                ,
                {%- endif %}
                {%- endfor %}
            )
            
            {%- if on_conflict_options.do_nothing %}
            DO NOTHING
            
            {%- elif on_conflict_options.do_update %}
            DO UPDATE SET
                {%- for column in on_conflict_options.update_columns %}
                {{ column }} = EXCLUDED.{{ column }}
                {%- if not loop.last %}
                ,
                {%- endif %}
                {%- endfor %}
            {%- endif %}
        {%- endif %}
        
        RETURNING
            *
    ''')

    sql = template.render(
        tablename=model.tablename,
        columns=values.columns,
        on_conflict_options=on_conflict_options
    )

    sql = ' '.join(sql.split())
    sql = sql.strip()

    return InsertSQL(
        sql,
        vars_
    )


def stream_insert(
        cursor: DictCursor,
        dataclass_type: type[_T],
        data: Iterable[_T],
        columns: list[str] = None,
        on_conflict_options: dict = None
) -> Generator[_T, None, None]:
    if not data:
        return

    insert_query = create_insert_query(
        dataclass_type,
        data,
        columns,
        on_conflict_options
    )

    execute_values(
        cursor,
        insert_query.sql,
        insert_query.vars
    )

    results = stream_from_cursor(cursor)
    results = stream_to_dataclass_type(results, dataclass_type)

    for result in results:
        yield result
