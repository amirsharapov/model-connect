from dataclasses import dataclass, field as dataclass_field
from typing import Any, TypeVar

from jinja2 import Template
from psycopg2.extras import DictCursor

from model_connect.integrations.psycopg2.common.processing import process_filter_options, process_sort_options, \
    process_pagination_options
from model_connect.integrations.psycopg2.common.streaming import stream_results_to_model_type, stream_from_cursor
from model_connect.integrations.psycopg2.options.model import Psycopg2Model
from model_connect.registry import get_model_field_options, get_model_options

_T = TypeVar('_T')


@dataclass
class SelectSQL:
    sql: str
    vars: list[Any] = dataclass_field(
        default_factory=list
    )


def create_select_query(
        model_class: type[_T],
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
) -> SelectSQL:
    vars_ = []

    model = get_model_options(model_class)
    model = model.integrations.get(Psycopg2Model)

    filter_options = process_filter_options(
        model_class,
        filter_options,
        vars_
    )
    filter_options = list(filter_options)

    sort_options = process_sort_options(
        model_class,
        sort_options
    )
    sort_options = list(sort_options)

    pagination_options = process_pagination_options(
        pagination_options,
        vars_
    )

    template = Template('''
        SELECT
            *

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


def stream_select(cursor: DictCursor, model_class: type[_T], chunk_size: int = 1000):
    query = create_select_query(model_class)

    cursor.execute(query.sql, query.vars)

    results = stream_from_cursor(cursor, chunk_size)
    results = stream_results_to_model_type(results, model_class)

    for result in results:
        yield result
