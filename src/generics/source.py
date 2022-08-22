from generics.generic import Generic
from abstract.settings import SettingsObject
from abc import abstractmethod

class SourceSettings(SettingsObject):

    def __init__(self):
        self.ticker_list: list[str] = []
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
        super().__init__(global_settings, None)


def load():
    util.unimplemented()

def list():
    util.unimplemented()