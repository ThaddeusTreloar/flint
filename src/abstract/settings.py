
from yaml import safe_load_all, safe_dump
from abc import abstractmethod, ABC

class SettingsObject(ABC):
    
    '''
    Abstract class to create settings objects for modules.
    Must implement:
        'interperateSetting(self, key: str, value: str) -> object'
        'validateConfig(self)'
    '''

    def loadConfigFile(self, file_path: str, namespace: str):

        self.overrideDefaults(self.readInConfig(file_path, namespace))

    @staticmethod
    def readInConfig(file_path: str, namespace: str) -> dict:
        
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

    def overrideDefaults(self, config: dict):

        # Rework this to function in a for loop on the dict.
        if config:

            for key, value in config.items():
                
                setattr(self, key, self.interperateSetting(key, value))
