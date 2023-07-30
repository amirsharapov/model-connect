from abc import ABC


class Base(ABC):
    """Helper class for tracking leftover args and kwargs."""
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
