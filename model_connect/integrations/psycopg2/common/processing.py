from dataclasses import dataclass
from typing import TypeVar, Optional

from model_connect import registry
from model_connect.constants import is_undefined, UNDEFINED
from model_connect.registry import get_model_field

_T = TypeVar('_T')


class ProcessedFilters(list['ProcessedFilter']):
    def __init__(self, vars_: list = UNDEFINED, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if is_undefined(vars_):
            vars_ = []

        self.vars = vars_


@dataclass
class ProcessedFilter:
    column: str
    operator: str
    value: str


class ProcessedSortingOptions(list['ProcessedSortingOption']):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


@dataclass
class ProcessedSortingOption:
    column: str
    direction: str


@dataclass
class ProcessedPaginationOptions:
    limit: Optional[int] = None
    skip: Optional[int] = None


def process_filter_options(
        dataclass_type: type[_T],
        filter_options: dict,
        vars_: list
) -> ProcessedFilters:
    result = ProcessedFilters(
        vars_
    )

    if not filter_options:
        return result

    for field, operators_object in filter_options.items():
        field = get_model_field(dataclass_type, field)

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

                result.vars.append(value)
                result.append(
                    ProcessedFilter(
                        column=field.name,
                        operator=operator,
                        value='%s'
                    )
                )

                continue

            if not isinstance(value, (list, set, tuple)):
                value = [value]

            for value_ in value:
                if value_ is None and operator == '=':
                    operator = 'IS'
                if value_ is None and operator in ('!=', '<>'):
                    operator = 'IS NOT'

                result.vars.append(value_)
                result.append(
                    ProcessedFilter(
                        column=field.name,
                        operator=operator,
                        value='%s'
                    )
                )

    return result


def process_sort_options(
        dataclass_type: type[_T],
        sort_options: dict
):
    result = ProcessedSortingOptions()

    if not sort_options:
        return result

    for field, direction in sort_options.items():
        field = get_model_field(dataclass_type, field)

        if not field:
            continue

        if not field.can_sort:
            continue

        direction = direction.upper()

        if direction not in ('ASC', 'DESC'):
            continue

        result.append(
            ProcessedSortingOption(
                column=field.name,
                direction=direction
            )
        )

    return result


def process_pagination_options(
        pagination_options: dict,
        vars_: list
):
    result = ProcessedPaginationOptions()

    if not pagination_options:
        return result

    if 'limit' in pagination_options:
        result.limit = pagination_options['limit']
        vars_.append(result.limit)

    if 'skip' in pagination_options:
        result.skip = pagination_options['skip']
        vars_.append(result.skip)

    return result


def process_group_by_options(
        dataclass_type: type[_T],
        group_by_options: list
):
    result = []

    model_fields = registry.get(dataclass_type).model_fields

    for column in group_by_options:
        if column not in model_fields:
            continue

        model_field = model_fields[column]

        if not model_field.can_group:
            continue

        result.append(model_field.name)

    return result
