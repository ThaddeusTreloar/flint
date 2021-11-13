from generics.generic import Generic
from abstract.settings import SettingsObject

class MLNN(Generic):

    local_save_command_set = {}

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)