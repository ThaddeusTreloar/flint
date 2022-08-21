import abstract.settings as s, util, error
from generics.kernel import Kernel
from abstract.settings import SettingsObject
from itertools import chain
from handlers.preprocess_handler import PreProcessHandler
from inspect import signature
from util import helpDialogue, kernel_exit
from typing import Iterator
from error import ModuleError

class CoreKernel(Kernel):

    @property
    def description(self):
        return 'The inbuilt core kernel.'

    def __init__(self, global_settings: SettingsObject):

        self.global_settings: SettingsObject = global_settings

        self.preprocess_module: Preprocess = PreProcessHandler(self.global_settings.plugins_dir)

        self.module_list: tuple(str) = ("input", "kernel", "mlnn", "output", "preprocess", "source")

        # Find some way to only have to enter
        self.local_command_set_: dict = {
            "save"      : {
                "input" : self.moduleLookup,
                "help"  : self.helpSave,
            },
            "preprocess" : self.preprocess_module.local_command_set,
            "test"      : self.test,
            "help"      : {
                "input": self.moduleLookup,
                "help" : self.help,
            },
            "exit"      : kernel_exit,
            "quit"      : kernel_exit,
        }

    @property
    def local_command_set(self) -> str:
        return self.local_command_set_
    
    def moduleLookup(self, module_parent: str):

        try_mod = module_parent+"_module"

        try:
            module_command_set = getattr(self.global_settings, (try_mod)).local_command_set
        except AttributeError:
            raise ModuleError("Module: '%s' is not a valid module..." % (module_parent))

        return module_command_set
    
    def execute(self, user_command: list[str], command_set=None) -> str:
        
        if not command_set:
            command_set = self.local_command_set
        
        user_command = [n for n in user_command]

        for index, item in enumerate(user_command):

            if callable(command_set[item]):
                if command_set[item].__name__ == "moduleLookup":
                    command_set = command_set[item](item)
                    user_command.insert(index+1, user_command[index-1])

                else:

                     if len(args) < 1:

                         if len(signature(current_item).parameters) < 1:

                             return command_set[item]()
                
                         else:

                             break

                    else:
                        return command_set[item](user_command[index+1:])

            else:
                command_set = command_set[item]
        
        raise StopIteration()

    def start(self):
        self.global_settings.output_module.submit({"body":"Welcome...\n\nType help for commands.\n"})
        self.global_settings.input_module.start()

    def submit(self, user_command: list[str]):
        try:
            result = self.execute(user_command)
            self.global_settings.output_module.submit({"body": result})
        except KeyError as K:
            self.global_settings.output_module.submit({"body": "Commmand '%s' not recognised..." % (K.args[0])})

        except StopIteration as S:
            result = self.execute(user_command + ["help"])
            self.global_settings.output_module.submit({"body": result})

        except ModuleError as M:
            self.global_settings.output_module.submit({"body": M.message})

    @staticmethod
    def test(s: list[str]) -> list[str]:
        return s

    @staticmethod
    def help() -> str:
        return "usage: <command> <args>\n\n\thelp: Display this help.\n\ttest: Returns provided arguments.\n\n\tquit/exit: Exit this program.\n"


    @staticmethod
    def helpSave(s: list[str]) -> str:
        # Unfinished. I'll do this later
        return helpDialogue(["usage: save <module> <args>", "", "<module>: Calls <module> 'save' kernel commands."])