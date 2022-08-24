from generics.generic import Generic
from abc import abstractmethod, ABC
from abstract.settings import SettingsObject

class KernelSettings(SettingsObject):

    @property
    def config_namespace(self):
        return "kernel"

    def __init__(self, config_path):
        self.daemoniseCallingThread = False
        super().__init__(config_path)


    def interperateSetting(self, key: str, value: str) -> object:
        match key:
            case "daemonise":
                return "daemoniseThread", self.boolFromString(value)
            case _:
                return key, value

class Kernel(ABC):

    def __init__(self, global_settings):
        self.local_settings = KernelSettings(global_settings.config_path)
        self.global_settings = global_settings

    @abstractmethod
    def execute(self):
        '''
        Kernel api call to execute commands.
        Allows the kernel to control what commands are callable by input methods.
        '''

    @abstractmethod
    def start(self, settings):
        '''
        Entry point for the kernel to start.
        '''
