from abstract import Handler, HandlerSettings
from generics import Preprocess
from pathlib import Path
from typing import Any


class PreProcessHandler(Handler):

    @property
    def module_type(self):
        return Preprocess

    @property
    def local_command_set(self) -> dict:
        return {
            "list": {
                "available": self.listAvailableModules,
                "commands": self.commands,
            },
            "help": self.help,
        }

    def __init__(self, settings: Any, parent_kernel):
        super().__init__(settings, parent_kernel)
        self.local_settings = HandlerSettings(
            self.global_settings.config_path, "preprocess")

    def start(self) -> None:
        ...

    def help() -> str:
        return "Todo"

    def submit(self):
        ...


'''
    @classmethod
    def createSequence(self):
   '''
