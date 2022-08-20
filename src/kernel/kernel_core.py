import abstract.settings as s, util, error
from generics.kernel import Kernel
from error import InsufficientArgumentsError
from abstract.settings import SettingsObject
from itertools import chain

class CoreKernel(Kernel):

    @property
    def description(self):
        return 'The inbuilt core kernel.'

    def __init__(self, global_settings: SettingsObject):
        self.command_set: dict = {
            "save"      : {
                "input" : global_settings.input_module.local_save_command_set,
                #"mlnn"   : global_settings.mlnn_module.local_command_set,
                "help"  : self.helpSave
            },
            "test"      : self.test,
            "help"      : self.help,
            "exit"      : util.kernel_exit,
            "quit"      : util.kernel_exit,
        }
        
        super().__init__(global_settings)

    def execute(self, user_command: dict, command_set=None):
        
        if not command_set:
            command_set = self.command_set

        current_item = command_set[next(user_command)]

        if callable(current_item):
            return current_item([n for n in user_command])
        else:
            return self.execute(user_command, current_item)


    def start(self):
        self.global_settings.output_module.submit({"body":"Welcome Alex, ya schlong...\n\nType help for commands.\n"})
        self.global_settings.input_module.start()

    def submit(self, user_command: str):
        try:
            result = self.execute(user_command)
            self.global_settings.output_module.submit({"body": result})
        except KeyError as K:
            self.global_settings.output_module.submit({"body": "Commmand '%s' not recognised..." % (K.args[0])})

        except StopIteration as S:
            result = self.execute(chain(user_command, ["help"]))
            self.global_settings.output_module.submit({"body": result})

        except InsufficientArgumentsError as I:
            raise I

    @staticmethod
    def test(s: [str]) -> [str]:
        return s

    @staticmethod
    def help(s: [str]) -> str:
        return "usage: <command> <args>\n\n\thelp: Display this help.\n\ttest: Returns provided arguments.\n\n\tquit/exit: Exit this program.\n"

    def helpSave(s: list[str]) -> str:
        # Unfinished. I'll do this later
        return "usage: save <module> <args>\n\n\tinput: Calls input save commands.\n\ttest: Returns provided arguments.\n\n\tquit/exit: Exit this program.\n"