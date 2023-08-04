from model_connect.globals.options.connect import GlobalConnectOptions
from model_connect.globals import registry


def connect_global_options(options: GlobalConnectOptions):
    options.resolve()
    registry.add(options)
