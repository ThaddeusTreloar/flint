from threading import Lock
from generics import Output
from abstract import Settings
from termcolor import colored
from generics.printer import Printer
from util import unimplemented


class Console(Output, Printer):

    def __init__(self, global_settings: Settings, parent_handler, print_lock: Lock):
        Output.__init__(self, global_settings, parent_handler)
        Printer.__init__(self, print_lock)

    def start(self):
        if not self.parent_handler.started:
            self.submit(
                {"body": "Welcome...\n\nType help for commands.\n"})

    def submit(self, response: dict) -> None:

        # self.print_lock.acquire()
        if response["body"] == None and self.global_settings.debug:
            # todo<0011>: log this.
            print(colored("!!FUNCTION WITH NO RETURN REPONSE!!", 'red'))
            print(colored("!!Potential misimplementation of function return!!", 'red'))

        print(response["body"], flush=True)
        # self.print_lock.release()

    @staticmethod
    def help() -> str:
        return "todo"

    @staticmethod
    def description() -> str:
        return 'An output module that returns all results back to the Command Line Interface'

    def exit(self) -> None:
        return None
