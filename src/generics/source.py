from generics import Generic
from abstract import Settings
from abc import abstractmethod

class SourceSettings(Settings):

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

    def __init__(self, global_settings: Settings):
        super().__init__(global_settings, None)


def load():
    util.unimplemented()

def list():
    util.unimplemented()