from generics.output import Output
from abstract.settings import SettingsObject
from util import unimplemented
class ConsoleOutput(Output):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

        self.local_command_set_ = {}

    @classmethod
    def submit(self, response: dict):

        print(response["body"])
        
        print(self.build_terminal_preamble(), end='')

    @staticmethod
    def build_terminal_preamble():

        buffer = "flint "

        buffer += ":: "

        return buffer

    def local_command_set(self):
        return self.local_command_set_

    def help(self, args) -> str:
        unimplemented()