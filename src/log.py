from abstract import Settings
from pathlib import Path
from logging import basicConfig, WARNING, INFO
from typing import Tuple, Any
from termcolor import colored


class LoggingSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "log"

    @property
    def defaultLogPath(self) -> Path:
        return (self.root_directory() / "flint.log").resolve()

    def __init__(self) -> None:

        self.log_path: Path = self.defaultLogPath
        self.log_level: int = WARNING
        self.active: bool = False

        super().__init__()

        if not self.checkLogPathAccessible():
            print(colored(
                "Log file path <%s> either in accessible or user does not have r/w permissions." % (self.log_path)))
            self.log_path = self.defaultLogPath

            if not self.checkLogPathAccessible():
                print(colored(
                    "Default log file path <%s> either in accessible or user does not have r/w permissions.\n\
                        Unable to initialise logging" % (self.log_path)))
                return None

        basicConfig(filename=self.log_path,
                    encoding="utf-8",
                    level=self.log_level,
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    format="%(levelname)s -> %(asctime)s : %(name)s :: %(message)s",
                    force=True)

        self.active = True

    def checkLogPathAccessible(self) -> bool:

        try:
            self.log_path.touch(exist_ok=True)
            return True

        except PermissionError or FileNotFoundError:
            return False

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "log_path":
                return key, self.ParseSettingsVariablesForProperties(key, value)
            case "log_level":
                match value:
                    case "CRITICAL":
                        return key, 50,
                    case "ERROR":
                        return key, 40
                    case "WARNING":
                        return key, 30
                    case "INFO":
                        return key, 20
                    case "DEBUG":
                        return key, 10
                    case "NOTSET":
                        return key, 0
                    case _:
                        # todo<0011>
                        print(
                            "%s not a valid log level. Defaulting to WARNING" % (value))
                        return key, 30
            case _:
                return key, value
