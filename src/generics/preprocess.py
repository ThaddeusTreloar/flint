from generics.generic import Generic
from abstract.settings import SettingsObject

class Preprocess(Generic):

    local_command_set = {}

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)