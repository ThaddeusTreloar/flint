from generics.input import Input
from abstract.settings import SettingsObject
from util import helpDialogue, unimplemented
import readline
import readline
from rlcompleter import Completer

class LocalCompleter(Completer):

    def __init__(self):

        nspace = {
            "save" : {
                "help": {},
                "hand" : {
                    "some"
                },
                "input": {},
            },
            "simple" : {},
            "pre" : {
                "set":{}
            }
        }

        super().__init__(nspace)

    def complete(self, text, state):
        """Return the next possible completion for 'text'.
        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.
        """

        if not text.strip():
            
            if state == 0:
                if _readline_available:
                    readline.insert_text('\t')
                    readline.redisplay()
                    return ''
                else:
                    return '\t'
            else:
                return None
        if state == 0:
            if " " in text:
                self.matches = self.ctx_matches(text)
            else:
                self.matches = self.global_matches(text)
        try:
            return self.matches[state]
        except IndexError:
            return None

    def global_matches(self, text):

        matches = []
        n = len(text)

        for nspace in [self.namespace]:
            for word, val in nspace.items():
                if word[:n] == text:
                    matches.append(word)

        return matches

    def ctx_matches(self, text):

        matches = []
        args = text.split(" ")
        
        subject = args.pop()

        nspace = self.namespace

        for arg in args:
            
            if nspace.__contains__(arg):
                nspace = nspace[arg]
            else:
                return None

        if text[-1] != " ":
            n = len(subject)
            for word in nspace.keys():    
                if word[:n] == subject:
                    matches.append(" ".join(args+[word]))
        else:
            for word in nspace.keys():    
                matches.append(" ".join(args+[word]))

        return matches


class Console(Input):

    @property
    def daemoniseThread(self):
        return False

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

        readline.set_completer(LocalCompleter().complete)
        readline.set_completer_delims("\n`~!@#$%^&*()-=+[{]}\|;:'\",<>/?")
        readline.parse_and_bind("tab: complete")

        while True:
            try:
                self.history.append(input(self.build_terminal_preamble()))
                self.submit(self.history[-1].split(" "))

            except KeyError as K:
                raise K

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
        return helpDialogue(["usage: save input <command> <args>", "", "history <path>: Save input history to <path>"])

    @classmethod
    def saveHistory(self, path: str) -> str:
        unimplemented()