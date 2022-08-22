from abstract.settings import SettingsObject
from pathlib import Path
from logging import basicConfig, WARNING, INFO

class LoggingSettings(SettingsObject):

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
        if key=="log_path":
            return self.ParseSettingsVariablesForProperties(key, value)
        elif key=="log_level":
            levels = {
                "CRITICAL": 50,
                "ERROR":40,
                "WARNING":30,
                "INFO":20,
                "DEBUG":10,
                "NOTSET":0,
            }
            try:
                return levels[value]
            except KeyError:
                print("%s not a valid log level. Defaulting to WARNING" % (value))