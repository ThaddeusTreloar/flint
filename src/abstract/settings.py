
from pathlib import Path
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC
from logging import error, warning
from pathlib import Path
from re import sub

class SettingsObject(ABC):
    
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

    def __init__(self, config_path=None):

        if not config_path:
            self._config_path = self.root_directory() / Path("config.yaml")
        else:
            self._config_path = config_path

        self.loadConfigFile(self.config_path, self.config_namespace)

    def loadConfigFile(self, file_path: str, namespace: str):

        self.overrideDefaults(self.readInConfig(file_path, namespace))

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
    
    def ParseSettingsVariablesForProperties(self, key: str,prop: str) -> str:
        #todo: clean this up
        if all(symbol in prop for symbol in ['<', '>']):
            prop = prop.split("<")
            for index, item in enumerate(prop):
                if ">" in item:
                    buffer = item.split(">")
                    if hasattr(self, buffer[0]):
                        value = getattr(self, buffer[0])
                        buffer[0] = value
                        prop[index] = buffer[0].__str__() + buffer[1]
                    else:
                        e = "Config error in %s.%s: Variable <%s> not found." % (self.config_namespace, key, buffer[0])
                        error(e)
                    
                        return Path(getattr(self, key))

            return Path("".join(prop))
        else:
            return prop

    def overrideDefaults(self, config: dict):

        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():
                if hasattr(self, key):
                    #value = sub(r'[^\w]', '', value.replace(" ", ""))
                    value = self.interperateSetting(key, value.replace(" ", ""))
                    if value != None:
                        setattr(self, key, value)
                else:
                    e = "Config error in %s: Setting <%s> does not exist." % (self.config_namespace, key)
                    warning(e+" Variable not set, skipping...")
                    continue

                
