from util import panic
from global_settings import GlobalSettings
from log import LoggingSettings
from inspect import getmembers, isclass
from abstract import Kernel
from pathlib import Path
from importlib.machinery import SourceFileLoader
from termcolor import colored
from tools import coupler
from typing import Optional

# Will need to implement a function to validate all extensions.
def validate_extensions():
    pass

# Will need to implement a function to load extensions.
def load_extensions():
    pass

def lookup_module(settings: GlobalSettings):

    # todo: review coupling?
    # todo<inconsistency>: Kernel modules are set in config by their module name 
    # but handler modules are set in the config by their class name. Consider revising.
    kernel_path = coupler(settings, "plugins_dir", Path("./src/inbuilt_plugins")) \
        / "kernel" / coupler(settings, "kernel_module", Path("CoreKernel"))

    if kernel_path.exists() and kernel_path.is_dir() and Path(kernel_path / Path('__init__.py')).exists():

        module_path: str = str(Path(kernel_path / Path('__init__.py')))

        module = SourceFileLoader(settings.kernel_module, module_path).load_module()

        return module

    else:
        
        return None

def prime_kernel(settings: GlobalSettings):

    kernel: Optional[Kernel] = lookup_module(settings)

    if kernel is None:

        if settings.kernel_module != "CoreKernel":
            #todo<0011>
            print(colored("Kernel module <%s> not found, falling back on <CoreKernel>..." \
                % (settings.kernel_module), 'red'))
            settings.kernel_module = "core_kernel"
            return prime_kernel(settings)

        else:
            panic(colored("Fallback kernel module failed to load. Either fix config \
                or load CoreKernel into plugins_dir. Unable to continue...", 'red'))

    else:
        for obj in getmembers(kernel, isclass):
            
            if issubclass(obj[1], Kernel):
                return obj[1](settings)
        else:
            if settings.kernel_module != "CoreKernel":
                #todo<0011>
                print(colored("Kernel object not found within module <%s>, \
                    falling back on <CoreKernel>..." % (settings.kernel_module), 'red'))
                settings.kernel_module = "core_kernel"
                return prime_kernel(settings)

            else:
                panic(colored("Fallback kernel module failed to load. \
                    Kernel object not found within module. Unable to continue...", 'red'))
        
    


def init() -> GlobalSettings:

    LoggingSettings()
    return prime_kernel(GlobalSettings())
