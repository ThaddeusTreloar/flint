from util import panic
from global_settings import GlobalSettings
from log import LoggingSettings
from inspect import getmembers, isclass
from abstract import Kernel
from pathlib import Path
from importlib.machinery import SourceFileLoader
from termcolor import colored
from tools import coupler
from typing import Optional, List
from types import ModuleType


def lookup_module(settings: GlobalSettings) -> Optional[ModuleType]:

    kernel_path = settings.plugins_dir / "kernel" / settings.kernel_module

    if kernel_path.exists() and kernel_path.is_dir() and Path(kernel_path / Path('__init__.py')).exists():

        module_path: str = str(kernel_path / Path('__init__.py'))

        module: ModuleType = SourceFileLoader(
            settings.kernel_module, module_path).load_module()

        return module

    else:

        return None


def prime_kernel(settings: GlobalSettings) -> Kernel:

    kernel_module: Optional[ModuleType] = lookup_module(settings)
    kernel: Optional[Kernel] = None

    if kernel_module is not None:

        for obj in getmembers(kernel_module, isclass):

            if issubclass(obj[1], Kernel):
                # todo: This call is unsafe
                k: Kernel = obj[1](settings)
                kernel = k

    if kernel is not None:

        return kernel

    elif settings.kernel_module != "CoreKernel":
        # todo<0011>
        print(colored(
            f"Kernel module <{settings.kernel_module}> not found, falling back on <CoreKernel>...", 'red'))
        settings.kernel_module = "core_kernel"
        return prime_kernel(settings)

    else:
        # todo<0011>
        panic(colored("Fallback kernel module failed to load. Either fix config \
            or load CoreKernel into plugins_dir. Unable to continue...", 'red'))
        exit()


def init() -> Kernel:

    logging_settings = LoggingSettings()
    global_settings = GlobalSettings()
    if logging_settings.active:
        global_settings.logging_settings = logging_settings
    return prime_kernel(global_settings)
