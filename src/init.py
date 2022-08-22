from error import ConfigLoadError
from util import panic
from global_settings import GlobalSettings
from log import LoggingSettings
from generics.generic import Generic
from inspect import getmembers, getmodule, isclass

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def prime_kernel(settings: GlobalSettings):

    kernel = settings.handler_tree['kernel']

    for obj in getmembers(kernel, isclass):

        if issubclass(obj[1], Generic) and getmodule(obj[1]) == kernel:
            return obj[1](settings)

def init() -> GlobalSettings:

    LoggingSettings()
    return prime_kernel(GlobalSettings())
