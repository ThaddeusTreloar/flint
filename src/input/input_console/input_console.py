from generics.input import Input
from abstract.settings import SettingsObject
from util import helpDialogue, unimplemented

class Console(Input):

    def __init__(self, global_settings: SettingsObject, parent_handler):
        super().__init__(global_settings, parent_handler)
        self.history: list[str] = []
        self.local_command_set_ = {
            "save"    : {
                "history" : self.saveHistory,
                "help"    : self.saveHelp,
            },
            "help"    : self.help,
        }

    @property
    def local_command_set(self) -> dict[str, object]:
        return self.local_command_set_

    @property
    def description(self):
        return "Input module used for interacting with the kernel via a Command Line Interface."

    def start(self):

        while True:
            try:
                self.history.append(input())
                self.submit(self.history[-1].split(" "))

            except KeyError as K:
                raise K

    @staticmethod
    def help() -> str:
        return helpDialogue(["available commands:", "", "save"])

    @staticmethod
    def saveHelp() -> str:
        return helpDialogue(["usage: save input <command> <args>", "", "history <path>: Save input history to <path>"])

    @classmethod
    def saveHistory(self, path: str) -> str:
        unimplemented()