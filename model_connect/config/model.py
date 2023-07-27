from model_connect.config.base import BaseConfig


class ModelConfig(BaseConfig):
    def __init__(
            self,
            name: str = None,
            description: str = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.name = name or type(self).__name__
        self.description = description or ''
