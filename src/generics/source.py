from generics.generic import Generic
from abstract.settings import SettingsObject
from abc import abstractmethod

class SourceSettings(SettingsObject):

    local_save_command_set = {}

    def __init__(self):
        self.ticker_list: [str] = []
        self.api_key: str = ""
        self.period_length: str = ""

    @classmethod
    def interperateSetting(self, key: str, value: str) -> object:
        return value

    @classmethod
    def validateLoadedConfig(self):
        util.unimplemented()

class Source(Generic):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    @property
    @abstractmethod
    def local_save_command_set(self) -> dict:
        '''
        Function that returns the module level command set for the kernel
        command, 'save'.
        '''

def load():
    util.unimplemented()

def list():
    util.unimplemented()