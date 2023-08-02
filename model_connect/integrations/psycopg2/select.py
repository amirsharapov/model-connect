from dataclasses import dataclass, field as dataclass_field
from functools import cache
from typing import Any, TypeVar

from jinja2 import Template
from psycopg2.extras import DictCursor

from model_connect import registry
from model_connect.integrations.psycopg2.common.processing import (
    process_filter_options,
    process_sort_options,
    process_pagination_options, process_group_by_options
)
from model_connect.integrations.psycopg2.common.streaming import (
    stream_to_dataclass_type,
    stream_from_cursor
)
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
        dataclass_type: type[_T],
        columns: list[str] = None,
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None,
        group_by_options: list[str] = None
) -> SelectSQL:
    vars_ = []

    model = get_model(dataclass_type, 'psycopg2')

    if columns is None:
        columns = generate_select_columns(
            dataclass_type
        )

    filter_options = process_filter_options(
        dataclass_type,
        filter_options,
        vars_
    )

    sort_options = process_sort_options(
        dataclass_type,
        sort_options
    )

    pagination_options = process_pagination_options(
        pagination_options,
        vars_
    )

    group_by_options = process_group_by_options(
        dataclass_type,
        group_by_options
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
        
        {%- if group_by_options %}
            GROUP BY
            {%- for option in group_by_options %}
            {{ option }}
            {%- if not loop.last %}
            ,
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
        pagination_options=pagination_options,
        group_by_options=group_by_options
    )

    sql = ' '.join(sql.split())
    sql = sql.strip()

    return SelectSQL(
        sql,
        vars_
    )


def create_select_count_query(
        dataclass_type: type[_T],
        filter_options: dict = None,
):
    vars_ = []

    filter_options = process_filter_options(
        dataclass_type,
        filter_options,
        vars_
    )

    model = get_model(dataclass_type, 'psycopg2')

    template = Template('''
    SELECT
        COUNT(*)
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
    ''')

    sql = template.render(
        tablename=model.tablename,
        filter_options=filter_options
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
        pagination_options: dict = None,
        group_by_options: list[str] = None
):
    query = create_select_query(
        dataclass_type,
        columns,
        filter_options,
        sort_options,
        pagination_options,
        group_by_options
    )

    cursor.execute(query.sql, query.vars)

    results = stream_from_cursor(cursor, chunk_size)
    results = stream_to_dataclass_type(results, dataclass_type)

    for result in results:
        yield result


def select_count(
        cursor: DictCursor,
        dataclass_type: type[_T],
        filter_options: dict = None,
) -> int:
    query = create_select_count_query(
        dataclass_type,
        filter_options
    )

    cursor.execute(
        query.sql,
        query.vars
    )

    return cursor.fetchone()[0]
