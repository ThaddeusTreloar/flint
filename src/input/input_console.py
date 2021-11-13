from generics.input import Input
from abstract.settings import SettingsObject

class ConsoleInput(Input):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)
        self.local_save_command_set_ = {
            "help" : self.helpSave
        }

    def local_save_command_set(self) -> dict[str, object]:
        return self.local_save_command_set_

    def start(self):

        while True:
            try:
                user_command = input().split(" ")
                self.submit(user_command, self.global_settings)

            except KeyError as K:
                raise K

            except StopIteration as S:
                print("Insufficient arguments")

    @staticmethod
    def helpSave(s: str) -> str:
        return "I'm over here now"