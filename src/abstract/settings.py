
from pathlib import Path
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC
from logging import error, warning
from pathlib import Path

class SettingsObject(ABC):
    
    '''
    Abstract class to create settings objects for modules.
    Must implement:
        'interperateSetting(self, key: str, value: str) -> object'
        'validateConfig(self)'
    '''

    def __init__(self):
        self.root_dir: Path = self.determineRootDirectory()

    def loadConfigFile(self, file_path: str, namespace: str):

        self.overrideDefaults(self.readInConfig(file_path, namespace))

    @staticmethod
    def determineRootDirectory() -> Path:

        # Path includes file name; src/abstract/settings.py
        current_dir: Path = Path(__file__).parent.resolve()
        while current_dir.name != 'flint':
            if current_dir.name == '/':
                print("Could not find project root directory")
                break
            current_dir = current_dir.parent

        return current_dir.resolve()

    @staticmethod
    def readInConfig(file_path: Path, namespace: str) -> dict:
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
        

    @abstractmethod
    def interperateSetting(self, key: str, value: str) -> object:
        
        Function used to interperate values listed in the config.
        This is called by the 'overrideDefaults'function while
        iterating through the config key/value pairs.
        Allows a SettingsObject to create different behaviour depending
        on the key being set. For example, one can create objects
        directly from the value of a particular key.
        
    '''
    
    def pathParseSettingsVariables(self, key: str,path: str) -> str:
        if all(symbol in path for symbol in ['<', '>']):
            path = path.split("<")
            for index, item in enumerate(path):
                if ">" in item:
                    buffer = item.split(">")
                    try:
                        value = getattr(self, buffer[0])
                        buffer[0] = value
                        path[index] = buffer[0].__str__() + buffer[1]
                    except AttributeError:
                        e = "Config error in %s.%s: Variable <%s> not found." % (self.namespace, key, buffer[0])
                        error(e)
                    
                        return Path(getattr(self, key))

            return Path("".join(path))
        else:
            return path

    def overrideDefaults(self, config: dict):

        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():
                try:
                    getattr(self, key)
                except AttributeError:
                    e = "Config error in %s: Setting <%s> does not exist." % (self.namespace, key)
                    warning(e+" Variable not set, skipping...")
                    continue

                setattr(self, key, self.interperateSetting(key, value))
