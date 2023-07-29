from abc import ABC


class Base(ABC):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
