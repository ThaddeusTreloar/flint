from generics.output import Output
from abstract.settings import SettingsObject

class ConsoleOutput(Output):

    @property
    def description(self):
        return 'An output module that returns all results back to the Command Line Interface'

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    @classmethod
    def submit(self, response: dict):

        print(response["body"])
        
        print(self.build_terminal_preamble(), end='')

    @staticmethod
    def build_terminal_preamble():

        buffer = "alchemist-sieve "

        buffer += ":: "

        return buffer