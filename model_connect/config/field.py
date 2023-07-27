from dataclasses import Field
from typing import Optional

from model_connect.config.base import BaseConfig


class FieldConfig(BaseConfig):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dataclass_field: Optional[Field] = None
