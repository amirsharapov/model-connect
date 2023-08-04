from dataclasses import dataclass

from model_connect.constants import UNDEFINED, coalesce


@dataclass
class FastAPIGlobalOptions:
    base_prefix: str = UNDEFINED

    def resolve(self):
        self.base_prefix = coalesce(
            self.base_prefix,
            None
        )