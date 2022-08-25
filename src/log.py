from abstract import Settings
from pathlib import Path
from logging import basicConfig, WARNING, INFO


class LoggingSettings(Settings):

    @property
    def config_namespace(self):
        return "log"

    def __init__(self):
        
        self.log_path: Path = (self.root_directory() / "flint.log").resolve()
        self.log_level: int = WARNING

        super().__init__()
        self.validateConfig()

    def validateConfig(self):
        if not self.log_path.exists():
            print("Log doesn't exist, creating log file at %s" % self.log_path)
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
        basicConfig(filename=self.log_path, 
        encoding="utf-8", 
        level=self.log_level, 
        datefmt="%m/%d/%Y %I:%M:%S %p",
        format="%(levelname)s -> %(asctime)s : %(name)s :: %(message)s",
        force=True)

    def interperateSetting(self, key: str, value: str) -> object:
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
                        print("%s not a valid log level. Defaulting to WARNING" % (value))
                        return key, 30
            case "_":
                return key, value