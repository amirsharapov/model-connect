from model_connect.config.registry import process_model

__all__ = [
    'connect'
]


def connect(class_: type) -> None:
    process_model(class_)
