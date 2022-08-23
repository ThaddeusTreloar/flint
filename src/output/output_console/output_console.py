from generics.output import Output
from abstract.settings import SettingsObject

from termcolor import colored
from util import unimplemented

class Console(Output):

    @property
    def daemoniseThread(self):
        return False

    @property
    def description(self):
        return 'An output module that returns all results back to the Command Line Interface'

    @property
    def local_command_set():
        return {}

    def __init__(self, global_settings: SettingsObject, parent_handler):
        super().__init__(global_settings, parent_handler)

    def submit(self, response: dict):
        
        if response["body"] == None and self.global_settings.debug:
            # todo<0011>: log this.
            print(colored("!!FUNCTION WITH NO RETURN REPONSE!!", 'red'))
            print(colored("!!Potential misimplementation of function return!!", 'red'))

        print(response["body"])



    def local_command_set(self):
        return self.local_command_set_

    def help(self, args) -> str:
        unimplemented()