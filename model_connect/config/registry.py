from dataclasses import is_dataclass, fields

from model_connect.config.model_connect import ModelConnectConfig
from model_connect.config.processed_field import ProcessedFieldConfig

_registry = {}


def get_config(model) -> ModelConnectConfig:
    return _registry[model]


def process_model(model):
    assert is_dataclass(model)

    config = getattr(
        model,
        '__model_connect_config__',
        None
    )

    assert isinstance(config, ModelConnectConfig) or config is None

    fields_ = {}

    for field in fields(model):
        fields_[field.name] = ProcessedFieldConfig(
            dataclass_field=field
        )

    _registry[model] = ModelConnectConfig(
        model=model,
        fields=fields_,
        config=config
    )
