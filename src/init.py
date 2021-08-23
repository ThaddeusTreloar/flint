from error import ConfigLoadError
from util import panic
import settings as s

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def init() -> (s.SettingsObject):

    settings = None

    try:
        settings = s.loadConfigFile("./config.yaml")

        if not settings.input:
            from input.console import ConsoleInput
            settings.input = ConsoleInput()
        if not settings.kernel:
            from kernel.kernel_core import CoreKernel
            settings.kernel = CoreKernel()

    except ConfigLoadError as err:
        # Failing to load the config will cause the program to panic.
        # Consider changing this bahaviour to fallback onto defaults?
        panic(err)

    return settings
