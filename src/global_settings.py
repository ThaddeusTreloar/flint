# This will have to be cleaned up at some point
import util

from abstract import Settings
from generics import Generic

from importlib import import_module, invalidate_caches
from pyclbr import readmodule
from inspect import getmembers, getmodule, isclass

from pathlib import Path
from pathlib import Path
from weakref import ref
from logging import warning, Logger, WARNING
from typing import Tuple, Any


class GlobalSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "global"

    def __init__(self) -> None:
        self.debug: bool = True
        self.plugins_dir:   Path = Path("./src/inbuilt_plugins")

        self.kernel_module = "CoreKernel"

        super().__init__()

        # todo: This is the tree that lists references to all available modules
        # self.available_module_tree

        self.max_threads: int = 20

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "debug":
                return key, self.boolFromString(value)
            case _:
                return key, value
