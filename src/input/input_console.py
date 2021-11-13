from generics.input import Input
from abstract.settings import SettingsObject
from util import helpDialogue, unimplemented

class ConsoleInput(Input):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)
        self.history: list[str] = []
        self.local_save_command_set_ = {
            "history" : self.saveHistory,
            "help"    : self.help,
        }

    @property
    def local_save_command_set(self) -> dict[str, object]:
        return self.local_save_command_set_

    def start(self):

        while True:
            try:
                self.history.append(input())
                self.submit(self.history[-1].split(" "), self.global_settings)

            except KeyError as K:
                raise K

            except StopIteration as S:
                print("Insufficient arguments")

    @staticmethod
    def help(s: str) -> str:
        return helpDialogue(["usage: save input <command> <args>", "", "history <path>: Save input history to <path>"])

    @classmethod
    def saveHistory(self, path: str) -> str:
        unimplemented()