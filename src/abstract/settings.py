
from pathlib import Path
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC
from logging import error, warning
from pathlib import Path
from re import sub
from typing import Tuple, Optional, List, Any


class Settings(ABC):

    '''
    Abstract class to create settings objects for modules.
    Must implement:
        'interperateSetting(self, key: str, value: str) -> object'
        'validateConfig(self)'
    '''

    @property
    @abstractmethod
    def config_namespace(self):
        pass

    @property
    def config_path(self):
        return self._config_path

    def __init__(self, config_path: Path = None):

        if not config_path:
            self._config_path = self.root_directory() / Path("config.yaml")
        else:
            self._config_path = config_path

        self.loadConfigFile(self.config_path, self.config_namespace)

    def loadConfigFile(self, file_path: Path, namespace: str):

        config: Optional[dict] = self.readInConfig(file_path, namespace)

        if config is not None:
            self.overrideDefaults(config)

    def root_directory(self) -> Path:
        if not hasattr(self, 'root_dir'):
            # Path includes file name; src/abstract/settings.py
            current_dir: Path = Path(__file__).parent.resolve()
            while current_dir.name != 'flint':
                if current_dir.name == '/':
                    print("Could not find project root directory")
                    break
                current_dir = current_dir.parent
            self.root_dir = current_dir.resolve()
            return self.root_dir
        else:
            return self.root_dir

    @staticmethod
    def readInConfig(file_path: Path, namespace: str) -> Optional[dict]:
        try:
            with open(file_path, "r") as file:
                # Calling next directly on the loaded config may result in unpredictable behaviour
                raw = next(safe_load_all(file))

                return raw[namespace]

        except FileNotFoundError as error:

            print("Config file not found, using default settings...")
            return None

    '''
    @abstractmethod
    def validateConfig(self): # todo: finish config validation
        
        Function used to validate loaded data.
        Called by '__new__' on instantiation
    '''

    @abstractmethod
    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        '''
        Function used to interperate values listed in the config.
        This is called by the 'overrideDefaults'function while
        iterating through the config key/value pairs.
        Allows a SettingsObject to create different behaviour depending
        on the key being set. For example, one can create objects
        directly from the value of a particular key.
        '''

    def ParseSettingsVariablesForProperties(self, key: str, prop: str) -> Path:

        while prop.find("<") >= 0:
            start, finish = prop.find("<"), prop.find(">")
            if hasattr(self, prop[start+1:finish]):
                prop = prop.replace(prop[start:finish+1],
                                    str(getattr(self, prop[start+1:finish])))
            else:
                # todo<0011>
                print("Property %s in settings %s.%s not found, ignoring..." %
                      (prop[start:finish+1], self.config_namespace, key))
                prop = prop.replace(prop[start:finish+1], "")

        return Path(prop)

    def overrideDefaults(self, config: dict):

        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():

                key, value = self.interperateSetting(
                    key, value.replace(" ", ""))

                if hasattr(self, key):

                    setattr(self, key, value)

                else:
                    e = "Config error in %s: Setting <%s> does not exist." % (
                        self.config_namespace, key)
                    warning(e+" Variable not set, skipping...")
                    continue

    @staticmethod
    def boolFromString(s: str, default: bool = False):
        match s.lower():
            case "true":
                return True
            case "false":
                return False
            case _:
                return default
