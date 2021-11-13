import abstract.settings as s, util, error
from generics.kernel import Kernel
from abstract.settings import SettingsObject
from itertools import chain
from util import helpDialogue, kernel_exit
from typing import Iterator
from error import ModuleError

class CoreKernel(Kernel):

    def __init__(self, global_settings: SettingsObject):

        super().__init__(global_settings)

        self.command_set: dict = {
            "save"      : self.moduleLookup,'''{
                "input" : ,
                #"mlnn"  : self.global_settings.mlnn_module.local_save_command_set,
                "source": self.global_settings.source_module.local_save_command_set,
                "help"  : self.helpSave
            },'''
            "test"      : self.test,
            "help"      : self.help,
            "exit"      : kernel_exit,
            "quit"      : kernel_exit,
        }

    @property
    def local_save_command_set(self) -> str:
        unimplemented()

    def moduleLookup(self, args: list[str]):

        if len(args) > 0:
            try_mod = args[0]+"_module"
            try:
                cs = getattr(self.global_settings, (try_mod)).local_save_command_set
            except AttributeError:
                raise ModuleError("Module: '%s' is not a valid module..." % (args[0]))
            return [(n for n in args[1:]), cs]

        raise StopIteration()        
    
    def execute(self, user_command: list[str], command_set=None):
        
        if not command_set:
            command_set = self.command_set

        current_item = command_set[next(user_command)]

        if callable(current_item):
            # DODGY, DODGY, DODGY ALL OVER
            ret = current_item([n for n in user_command])
            # IS IT A A STRING OR A LIST, IDC. JUST DO A THING, AHOLE.
            if type(ret[0]) != str:
                return self.execute(ret[0], ret[1])
            else:
                return ret
        else:
            return self.execute(user_command, current_item)


    def start(self):
        self.global_settings.output_module.submit({"body":"Welcome Alex, ya schlong...\n\nType help for commands.\n"})
        self.global_settings.input_module.start()

    def submit(self, user_command: list[str]):
        try:
            result = self.execute(n for n in user_command)
            self.global_settings.output_module.submit({"body": result})
        except KeyError as K:
            self.global_settings.output_module.submit({"body": "Commmand '%s' not recognised..." % (K.args[0])})

        except StopIteration as S:
            result = self.execute(n for n in user_command + ["help"])
            self.global_settings.output_module.submit({"body": result})

        except ModuleError as M:
            self.global_settings.output_module.submit({"body": M.message})

    @staticmethod
    def test(s: [str]) -> [str]:
        return s

    @staticmethod
    def help(s: [str]) -> str:
        return helpDialogue(["usage: <command> <args>", "", "help: Display this help.", "test: Returns provided arguments.", "", "quit/exit: Exit this program."])

    @staticmethod
    def helpSave(s: list[str]) -> str:
        # Unfinished. I'll do this later
        return helpDialogue(["usage: save <module> <args>", "", "<module>: Calls <module> 'save' kernel commands."])