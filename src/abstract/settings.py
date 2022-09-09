
from sys import argv
from pathlib import Path
from termcolor import colored
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC
from logging import error, warning
from pathlib import Path
from re import sub
from typing import Tuple, Optional, List, Any, Dict


class Settings(ABC):

    '''
    Abstract class to create settings objects for modules.
    Note: ALL SETTINGS AVAILALE IN A CONFIG FILE MUST BE SET BEFORE CALLING super().__init__()
    Must implement:
        @property config_namespace (the namespace in the config file that addresses relevant settings)
        @method interperateSetting (this function is call by the parent construct when reading in the 
            config.)
    Handy tools:
        method boolFromString (converts a string to bool defaulting to provided value)
        when parsing config, will pickup settings values of format <attr> in a value.
            the class will search the class attributes for an attribute called 'attr' 
            and replace with the stored value if found. Will delete the call if 
            no value is found in class.
    '''

    @property
    @abstractmethod
    def config_namespace(self) -> str:
        '''
        Subsection of config to look for relevant settings
        '''
        pass

    @property
    def config_path(self) -> Path:
        return self._config_path

    def __init__(self, config_path: Optional[Path] = None) -> None:
        if config_path is None:
            self._config_path = self.root_directory() / Path("config.yaml")
        else:
            self._config_path = config_path

        self.loadConfigFile(self.config_path, self.config_namespace)

        self.userOverride()

    def userOverride(self) -> None:
        systemArguments = [x for x in argv]
        del systemArguments[0]

        for arg in systemArguments:
            kv_pair = arg.split("=")

            if len(kv_pair) != 2:
                continue

            match kv_pair[0].split("."):
                case [self.config_namespace, key]:
                    self.setSetting(key, kv_pair[1])

    def loadConfigFile(self, file_path: Path, namespace: str) -> None:

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
                raw_config: Dict = next(safe_load_all(file))

                if raw_config.__contains__(namespace):

                    return raw_config[namespace]
                else:
                    # todo<0011>
                    return None

        except FileNotFoundError as error:

            print("Config file not found, using default settings...")
            return None

    @abstractmethod
    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        '''
        Function used to interperate values listed in the config.
        Allows the child class to handle different settings in their own way.
        Suggest:
            def interperateSetting(self, key, value) -> Tuple[str, Any]
                match key:
                    case ...:
                        ...
                    case _:
                        key, value
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

    def overrideDefaults(self, config: dict) -> None:
        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():
                if value is str:
                    value = value.replace(" ", "")

                key, value = self.interperateSetting(
                    key, value)

                if hasattr(self, key):

                    setattr(self, key, value)

                else:
                    e = "Config error in %s: Setting <%s> does not exist." % (
                        self.config_namespace, key)
                    warning(e+" Variable not set, skipping...")
                    continue

    def setSetting(self, key: str, value: str) -> None:
        if hasattr(self, key):
            setattr(self, *self.interperateSetting(key, value))
        else:
            # todo<0011>: logging
            print(
                colored(f"!!{self.__class__.__name__} settings has no option: '{key}'!!", "red"))

    @staticmethod
    def boolFromString(s: str, default: bool = False) -> bool:
        match s.lower():
            case "true":
                return True
            case "false":
                return False
            case _:
                return default
