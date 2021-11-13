from generics.generic import Generic
from abstract.settings import SettingsObject

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

def load():
    util.unimplemented()

def list():
    util.unimplemented()