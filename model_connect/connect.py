from dataclasses import is_dataclass

from model_connect.options.connect import ConnectOptions

from model_connect import registry


def connect(dataclass_type: type, options: ConnectOptions = None):
    assert is_dataclass(dataclass_type)

    if options is None:
        options = ConnectOptions()

    options.resolve(dataclass_type)

    registry.add(
        dataclass_type,
        options
    )

    return dataclass_type
