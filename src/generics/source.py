from generics.generic import Generic
from abstract.settings import SettingsObject

class SourceSettings(SettingsObject):

    def __init__(self):
        self.ticker_list: [str] = []
        self.api_key: str = ""
        self.period_length: str = ""

    @classmethod
    def interperateSetting(self, key: str, value: str) -> object:
        return value

    @classmethod
    def validateLoadedConfig(self):
        pass

class Source(Generic):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

def load():
    pass

def list():
    pass