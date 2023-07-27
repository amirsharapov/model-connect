from dataclasses import dataclass, field

from typing import TypeVar
from unittest import TestCase

from model_connect import connect

_T = TypeVar('_T')


class Test(TestCase):
    def test(self):
        ...


@dataclass
class Person:
    id: int = field(default=None)
    name: str = field(default=None)
    age: int = field(default=None)


connect(Person)
