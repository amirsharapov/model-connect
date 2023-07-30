from enum import Enum

UNDEFINED = object()


def is_undefined(value):
    return value is UNDEFINED


def coalesce(*args):
    for arg in args:
        if not is_undefined(arg) and arg is not None:
            return arg


class HTTPMethods(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


def iter_http_methods():
    for method in HTTPMethods:
        yield method.value
