from error import ConfigLoadError
from util import panic
from settings import SettingsObject, loadConfigFile, validateLoadedConfig

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def init() -> SettingsObject:

    settings = loadConfigFile("./config.yaml")
    settings = validateLoadedConfig(settings)

    return settings
