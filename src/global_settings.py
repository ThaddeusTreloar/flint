from abstract import Settings
from generics import Generic
from log import LoggingSettings

from pathlib import Path
from typing import Tuple, Any, Optional


class GlobalSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "global"

    def __init__(self) -> None:
        self.debug: bool = True
        self.plugins_dir:   Path = Path("./src/inbuilt_plugins")
        self.logging_settings: Optional[LoggingSettings] = None

        self.kernel_module = "CoreKernel"

        self.max_threads: int = 20

        super().__init__()

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "debug":
                return key, self.boolFromString(value)
            case _:
                return key, value
