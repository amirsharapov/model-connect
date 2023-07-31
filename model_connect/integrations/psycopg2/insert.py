from dataclasses import dataclass, field, asdict
from typing import Iterable, TypeVar

from jinja2 import Template
from psycopg2.extras import DictCursor

from model_connect import registry
from model_connect.integrations.psycopg2 import Psycopg2Model, Psycopg2ModelField
from model_connect.integrations.psycopg2.common.streaming import stream_from_cursor, stream_results_to_model_type
from model_connect.registry import get_model_options

_T = TypeVar('_T')


@dataclass
class InsertSQL:
    sql: str
    vars: list = field(
        default_factory=list
    )


def create_insert_query(
        model_class: type[_T],
        data: _T | Iterable[_T],
        columns: list[str] = None
) -> InsertSQL:
    vars_ = []

    model = get_model_options(model_class)
    model = model.integrations.get(Psycopg2Model)

    if isinstance(data, model_class):
        data = [data]

    if not columns:
        model_fields = registry.get(model_class).model_fields.values()

        columns = []
        for model_field in model_fields:
            model_field = model_field.integrations.get(Psycopg2ModelField)

            if not model_field.include_in_insert:
                continue

            columns.append(
                model_field.column_name
            )

    values = []

    for item in data:
        if not isinstance(item, dict):
            # noinspection PyDataclass
            item = asdict(item)

        values.append(
            tuple(
                item[column] for
                column in
                columns
            )
        )

    vars_.extend(values)

    template = Template('''
        INSERT INTO
            {{ tablename }}
            (
                {%- for column_name in column_names %}
                    {{ column_name }}
                    {%- if not loop.last %}
                        ,
                    {%- endif %}
                {%- endfor %}
            )
        VALUES
            %s
        RETURNING
            *
    ''')

    sql = template.render(
        tablename=model.tablename,
        column_names=columns
    )

    sql = ' '.join(sql.split())
    sql = sql.strip()

    return InsertSQL(
        sql,
        vars_
    )


def stream_insert(
        cursor: DictCursor,
        model_class: type[_T],
        data: _T | Iterable[_T],
        columns: list[str] = None
) -> None:
    insert_query = create_insert_query(
        model_class,
        data,
        columns
    )

    cursor.executemany(
        insert_query.sql,
        insert_query.vars
    )

    results = stream_from_cursor(cursor)
    results = stream_results_to_model_type(results, model_class)

    for result in results:
        yield result
