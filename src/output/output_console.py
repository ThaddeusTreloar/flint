from generics.output import Output
from abstract.settings import SettingsObject

from termcolor import colored
from util import unimplemented

class ConsoleOutput(Output):

    @property
    def description(self):
        return 'An output module that returns all results back to the Command Line Interface'

    def __init__(self, global_settings: SettingsObject):
        self.global_settings = global_settings

        self.local_command_set_ = {}

    def submit(self, response: dict):
        
        if response["body"] == None and self.global_settings.debug:
            # todo<0011>: log this.
            print(colored("!!FUNCTION WITH NO RETURN REPONSE!!", 'red'))
            print(colored("!!Potential misimplementation of function return!!", 'red'))

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