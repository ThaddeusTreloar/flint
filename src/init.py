from error import ConfigLoadError
from util import panic
from global_settings import GlobalSettings
from log import LoggingSettings

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def init() -> GlobalSettings:

    LoggingSettings()
    return GlobalSettings()
