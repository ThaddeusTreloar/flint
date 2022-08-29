from generics import Input
from generics.input import LocalCompleter
from abstract import Settings
from util import helpDialogue, unimplemented
import readline


class Console(Input):

    @property
    def local_command_set(self) -> dict:
        return {
            "save": {
                "history": self.saveHistory,
                "help": self.saveHelp,
            },
        }

    @property
    def completes(self):
        return True

    @property
    def completer(self):
        return self._completer

    @property
    def daemoniseThread(self):
        return False

    def __init__(self, global_settings: Settings, parent_handler, handler_thread_queue, completionCommandTree: dict = None):
        super().__init__(global_settings, parent_handler,
                         handler_thread_queue)
        self.history: list[str] = []

        self._completer = LocalCompleter(completionCommandTree)
        readline.set_completer(self.completer.complete)
        readline.set_completer_delims("\n`~!@#$%^&*()-=+[{]}\|;:'\",<>/?")
        readline.parse_and_bind("tab: complete")

    @property
    def description(self):
        return "Input module used for interacting with the kernel via a Command Line Interface."

    def start(self):

        while True:
            try:
                match self.checkAndActionQueue():
                    case "exit":
                        break
                    case _:
                        self.submit(self.__class__.__name__, input(
                            self.build_terminal_preamble()).split(" "))
            except KeyboardInterrupt:
                print("here")
                self.submit(self.__class__.__name__, ["exit"])
            except EOFError:
                print("here")

    @staticmethod
    def build_terminal_preamble():

        buffer = "flint "

        buffer += ":: "

        return buffer

    @staticmethod
    def help() -> str:
        return helpDialogue(["available commands:", "", "save"])

    @staticmethod
    def saveHelp() -> str:
        return helpDialogue(["usage: save history <command> <args>", "", "history <path>: Save input history to <path>"])

    @classmethod
    def saveHistory(self, path: str) -> str:
        unimplemented()
