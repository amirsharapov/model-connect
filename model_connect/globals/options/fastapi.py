from dataclasses import dataclass

from model_connect.constants import UNDEFINED, coalesce


@dataclass
class FastAPIGlobalOptions:
    base_prefix: str = UNDEFINED
    default_resource_version: int = UNDEFINED

    def resolve(self):
        self.base_prefix = coalesce(
            self.base_prefix,
            None
        )

        self.default_resource_version = coalesce(
            self.default_resource_version,
            None
        )
