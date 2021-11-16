from abstract.settings import SettingsObject
from pathlib import Path
from logging import basicConfig, WARNING, INFO

class LoggingSettings(SettingsObject):

    def __init__(self):
        self.config_path: Path = (self.root_dir / "config.yaml").resolve()
        self.log_path: Path = (self.root_dir / "flint.log")
        self.log_level: int = WARNING
        self.namespace: str = "log"

    @classmethod
    def validateConfig(self):
        basicConfig(filename=self.log_path, 
        encoding="utf-8", 
        level=self.log_level, 
        datefmt="%m/%d/%Y %I:%M:%S %p",
        format="%(levelname)s -> %(asctime)s : %(name)s :: %(message)s",
        force=True)

    @classmethod
    def overrideDefaults(self, config: dict):
        try:
            self.log_path = self.interperateSetting("log_path", config["log_path"])
        except KeyError:
            pass
        try:
            self.log_level = self.interperateSetting("log_level", config["log_level"])
        except KeyError:
            pass

    @classmethod
    def interperateSetting(self, key: str, value: str) -> object:
        if "path" in key:
            return self.pathParseSettingsVariables(key, value)
        elif "level" in key:
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