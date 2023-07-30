from dataclasses import dataclass
from typing import Any, TypeVar

from model_connect.integrations.psycopg2.commons import stream_results_to_model_type, stream_from_cursor
from model_connect.registry import get_options


_T = TypeVar('_T')


@dataclass
class SelectQuery:
    query: str
    vars: tuple[Any, ...] | dict[str, Any] | list[Any] = None


def process_filter_options(
        dataclass_type: type[_T],
        filter_options: dict,
        vars_: list
):
    for field, value in filter_options.items():
        field = get_model_field(dataclass_type, field)

        if not field:
            continue

        if not field.can_filter:
            continue

        if isinstance(value, dict):
            operator = next(iter(value))
            value = value[operator]

        elif isinstance(value, (list, set, tuple)):
            operator = 'IN'
            value = tuple(value)

        else:
            operator = '='

        if value is None:
            if operator == '=':
                operator = 'IS'
            if operator in ('!=', '<>'):
                operator = 'IS NOT'

        vars_.append(value)

        yield {
            'column': field.name,
            'operator': operator,
            'value': '%s'
        }


def process_sort_options(
        cls: type[_T],
        sort_options: dict
):
    options = []

    for field, direction in sort_options.items():
        field = get_model_field(cls, field)

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


def create_select_query_template() -> SelectQuery:
    ...


def create_select_query(
        model_class: type[_T],
        filter_options: dict = None,
        sort_options: dict = None,
        pagination_options: dict = None
) -> SelectQuery:
    vars_ = []

    config = get_options(model_class)

    # pull from configs!
    tablename = model_class.__name__.lower()

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

        WHERE
            1 = 1
            {%- if filter_options is not none %}
            {%- for key, operator, value in filter_options %}
            AND {{ key }} {{ operator }} %s
            {%- endfor %}
            {%- endif %}

        ORDER BY
            {%- if sort_options is not none %}
            {%- for key, direction in sort_options %}
            {{ key }} {{ value }}
            {%- endfor %}
            {%- endif %}

        LIMIT
            {%- if pagination_options.limit is not none %}
            %s
            {%- endif %}

        OFFSET
            {%- if pagination_options.offset is not none %}
            %s
            {%- endif %}
        ;
        ''')

    query = template.render(
        tablename=tablename,
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
