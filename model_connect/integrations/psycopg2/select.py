from dataclasses import dataclass, field as dataclass_field
from functools import cache
from typing import Any, TypeVar

from jinja2 import Template
from psycopg2.extras import DictCursor

from model_connect import registry
from model_connect.integrations.psycopg2.common.processing import (
    process_filter_options,
    process_sort_options,
    process_pagination_options
)
from model_connect.integrations.psycopg2.common.streaming import stream_results_to_dataclass, stream_from_cursor
from model_connect.integrations.psycopg2.options.model import Psycopg2Model
from model_connect.registry import get_model

_T = TypeVar('_T')


@dataclass
class SelectSQL:
    sql: str
    vars: list[Any] = dataclass_field(
        default_factory=list
    )


@cache
def generate_select_columns(model_class: type[_T]) -> list[str]:
    columns = []

    model_fields = registry.get(model_class).model_fields.values()

    for model_field in model_fields:
        model_field = model_field.integrations.get('psycopg2')

        if not model_field.include_in_select:
            continue

        columns.append(
            model_field.column_name
        )

    return columns


def create_select_query(
        model_class: type[_T],
        columns: list[str] = None,
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
) -> SelectSQL:
    vars_ = []

    model = get_model(model_class, 'psycopg2')

    if columns is None:
        columns = generate_select_columns(
            model_class
        )

    filter_options = process_filter_options(
        model_class,
        filter_options,
        vars_
    )

    sort_options = process_sort_options(
        model_class,
        sort_options
    )

    pagination_options = process_pagination_options(
        pagination_options,
        vars_
    )

    template = Template('''
        SELECT
            {%- for column in columns %}
            {{ column }}
            {%- if not loop.last %}
            ,
            {%- endif %}
            {%- endfor %}

        FROM
            {{ tablename }}

        {%- if filter_options %}
            WHERE
            {%- for filter in filter_options %}
            {{ filter.column }} {{ filter.operator }} %s
            {%- if not loop.last %}
            AND
            {%- endif %}
            {%- endfor %}
        {%- endif %}

        {%- if sort_options %}
            ORDER BY
            {%- for option in sort_options %}
            {{ option.column }} {{ option.direction }}
            {%- if not loop.last -%}
            ,
            {%- endif -%}
            {%- endfor %}
        {%- endif %}

        {%- if pagination_options.limit %}
            LIMIT %s
        {%- endif %}

        {%- if pagination_options.offset %}
            OFFSET %s
        {%- endif %}
        ''')

    sql = template.render(
        columns=columns,
        tablename=model.tablename,
        filter_options=filter_options,
        sort_options=sort_options,
        pagination_options=pagination_options
    )

    sql = ' '.join(sql.split())
    sql = sql.strip()

    return SelectSQL(
        sql,
        vars_
    )


def stream_select(
        cursor: DictCursor,
        dataclass_type: type[_T],
        columns: list[str] = None,
        chunk_size: int = 1000,
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
):
    query = create_select_query(
        dataclass_type,
        columns,
        filter_options,
        sort_options,
        pagination_options
    )

    cursor.execute(query.sql, query.vars)

    results = stream_from_cursor(cursor, chunk_size)
    results = stream_results_to_dataclass(results, dataclass_type)

    for result in results:
        yield result


def stream_select_distinct(
        cursor: DictCursor,
        dataclass_type: type[_T],
        column: str,
        chunk_size: int = 1000,
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
):
    query = create_select_query(
        dataclass_type,
        [column],
        filter_options,
        sort_options,
        pagination_options
    )

    cursor.execute(query.sql, query.vars)

    results = stream_from_cursor(cursor, chunk_size)

    for result in results:
        yield result[column]
