from abstract import Settings
from pathlib import Path
from logging import basicConfig, WARNING, INFO
from typing import Tuple, Any


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

        super().__init__()
        self.validateConfig()

    def validateConfig(self) -> None:
        if not self.log_path.exists():
            # todo<0011>
            print("Log doesn't exist, creating log file at %s" % self.log_path)
            try:
                self.log_path.touch()
            except PermissionError:
                # todo<0011>
                print(
                    "Permission denied for: %s. Reverting to default logpath..." % self.log_path)
                self.log_path = self.defaultLogPath
                return self.validateConfig()
        basicConfig(filename=self.log_path,
                    encoding="utf-8",
                    level=self.log_level,
                    datefmt="%m/%d/%Y %I:%M:%S %p",
                    format="%(levelname)s -> %(asctime)s : %(name)s :: %(message)s",
                    force=True)

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

        return key, value
