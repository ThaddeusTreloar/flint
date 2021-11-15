
from pathlib import Path
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC

class SettingsObject(ABC):
    
    '''
    Abstract class to create settings objects for modules.
    Must implement @classmethods:
        'interperateSetting(self, key: str, value: str) -> object'
        'validateConfig(self)'
    '''

    def __new__(self):

        self.root_dir:     Path = self.determineRootDirectory()
        self.source_dir:   Path = self.root_dir / "src"

        self.__init__(self)
        self.loadConfigFile(self.config_path, self.namespace)
        self.validateConfig()

        return self

    @classmethod
    def loadConfigFile(self, file_path: Path, namespace: str):

        self.overrideDefaults(self.readInConfig(file_path, namespace))

    def determineRootDirectory() -> Path:

        # Path includes file name; src/abstract/settings.py
        current_dir: Path = Path(__file__).parent.resolve()
        while current_dir.name != 'flint':
            if current_dir.name == '/':
                print("Could not find project root directory")
                break
            current_dir = current_dir.parent

        return current_dir.resolve()

    def readInConfig(file_path: Path, namespace: str) -> dict:
        
        try:
            with open(file_path, "r") as file:
                # Calling next directly on the loaded config may result in unpredictable behaviour
                raw = next(safe_load_all(file))

                return raw[namespace]
        
        except FileNotFoundError as error:

            print("Config file not found, using default settings...")
            return None

    @classmethod
    @abstractmethod
    def validateConfig(self):
        '''
        Function used to validate loaded data.
        Called by '__new__' on instantiation
        '''

    @classmethod
    @abstractmethod
    def interperateSetting(self, key: str, value: str) -> object:
        '''
        Function used to interperate values listed in the config.
        This is called by the 'overrideDefaults'function while
        iterating through the config key/value pairs.
        Allows a SettingsObject to create different behaviour depending
        on the key being set. For example, one can create objects
        directly from the value of a particular key.
        '''

    @classmethod
    def overrideDefaults(self, config: dict):

        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():
                
                setattr(self, key, self.interperateSetting(key, value))
