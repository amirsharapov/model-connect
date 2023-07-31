from dataclasses import dataclass, field as dataclass_field
from inspect import isgenerator
from typing import Any, TypeVar

from jinja2 import Template

from model_connect.integrations.psycopg2.commons import stream_results_to_model_type, stream_from_cursor
from model_connect.integrations.psycopg2.options.model import Psycopg2Model
from model_connect.registry import get_model_field_options, get_model_options

_T = TypeVar('_T')


@dataclass
class SelectQuery:
    query: str
    vars: list[Any] = dataclass_field(
        default_factory=list
    )


def process_filter_options(
        dataclass_type: type[_T],
        filter_options: dict,
        vars_: list
):
    if not filter_options:
        return

    for field, operators_object in filter_options.items():
        field = get_model_field_options(dataclass_type, field)

        if not field:
            continue

        if not field.can_filter:
            continue

        if isinstance(operators_object, (list, set, tuple)):
            values = operators_object
            operators_object = {
                'IN': tuple(values)
            }

        if not isinstance(operators_object, dict):
            value = operators_object
            operators_object = {
                '=': value
            }

        for operator, value in operators_object.items():
            operator = operator.upper()

            if operator in ('IN', 'NOT IN'):
                value = tuple(value)
                vars_.append(value)

                yield {
                    'column': field.name,
                    'operator': operator,
                    'value': '%s'
                }

                continue

            if not isinstance(value, (list, set, tuple)):
                value = [value]

            for value_ in value:
                if value_ is None and operator == '=':
                    operator = 'IS'
                if value_ is None and operator in ('!=', '<>'):
                    operator = 'IS NOT'

                vars_.append(value_)

                yield {
                    'column': field.name,
                    'operator': operator,
                    'value': '%s'
                }


def process_sort_options(
        cls: type[_T],
        sort_options: dict
):
    if not sort_options:
        return

    for field, direction in sort_options.items():
        field = get_model_field_options(cls, field)

        if not field:
            continue

        if not field.can_sort:
            continue

        direction = direction.upper()

        if direction not in ('ASC', 'DESC'):
            continue

        yield {
            'column': field.name,
            'direction': direction
        }


def process_pagination_options(
        pagination_options: dict,
        vars_: list
):
    if not pagination_options:
        return

    result = {}

    if not pagination_options:
        return result

    if 'limit' in pagination_options:
        result['limit'] = pagination_options['limit']
        vars_.append(result['limit'])

    if 'offset' in pagination_options:
        result['offset'] = pagination_options['offset']
        vars_.append(result['offset'])

    return result


def create_select_query(
        model_class: type[_T],
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
) -> SelectQuery:
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

    query = template.render(
        tablename=model.tablename,
        filter_options=filter_options,
        sort_options=sort_options,
        pagination_options=pagination_options
    )

    return SelectQuery(
        query=query,
        vars=vars_
    )


def stream_select(model_class: type[_T], cursor: Any, chunk_size: int = 1000):
    query = create_select_query(model_class)

    cursor.execute(query.query, query.vars)

    results = stream_from_cursor(cursor, chunk_size)
    results = stream_results_to_model_type(results, model_class)

    for result in results:
        yield result
