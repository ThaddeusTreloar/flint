from abstract.handler import Handler
from generics.preprocess import Preprocess
from global_settings import GlobalSettings
from pathlib import Path

class PreProcessHandler(Handler):

    @property
    def module_type(self):
        return Preprocess

    @property
    def plugins_dir_slug(self) -> str:
        return "preprocess"

    @property
    def local_command_set(self) -> dict:
        return {
            "list"  : self.listAvailableModules,
            "help"  : self.help,
        }

    def __init__(self, settings: GlobalSettings, parent_kernel):
        super().__init__(settings, parent_kernel)

    def help() -> str:
        return "Todo"

    def submit(self):
        pass
'''
    @classmethod
    def createSequence(self):
   '''     