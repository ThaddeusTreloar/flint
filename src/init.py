from error import ConfigLoadError
from util import panic
from global_settings import GlobalSettings
from log import LoggingSettings
from generics.generic import Generic
from inspect import getmembers, getmodule, isclass
from generics.kernel import Kernel
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from termcolor import colored

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def lookup_module(settings: GlobalSettings):

    kernel_path = settings.plugins_dir / Path("kernel") / Path(settings.kernel_module)

    if (kernel_path).is_dir():
        spec = spec_from_file_location(kernel_path.name, kernel_path / Path(kernel_path.name + '.py'))
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        return module

def prime_kernel(settings: GlobalSettings):

    kernel = lookup_module(settings)

    for obj in getmembers(kernel, isclass):
        
        if issubclass(obj[1], Kernel):
            return obj[1](settings)
        
    if settings.kernel_module != "CoreKernel":
        #todo<0011>
        print(colored("Kernel module <%s> not found, falling back on <CoreKernel>..." % (settings.kernel_module), 'red'))
        settings.kernel_module = "CoreKernel"
        return prime_kernel(settings)

    else:
        panic(colored("Fallback kernel module failed to load. Unable to continue...", 'red'))


def init() -> GlobalSettings:

    LoggingSettings()
    return prime_kernel(GlobalSettings())
