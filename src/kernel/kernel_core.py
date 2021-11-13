import abstract.settings as s, util, error
from generics.kernel import Kernel
from abstract.settings import SettingsObject
from itertools import chain

class CoreKernel(Kernel):

    def __init__(self, global_settings: SettingsObject):

        super().__init__(global_settings)

        self.command_set: dict = {
            "save"      : {
                "input" : self.global_settings.input_module.local_save_command_set(),
                #"mlnn"  : self.global_settings.mlnn_module.local_save_command_set,
                "source": self.global_settings.source_module.local_save_command_set(),
                "help"  : self.helpSave
            },
            "test"      : self.test,
            "help"      : self.help,
            "exit"      : util.kernel_exit,
            "quit"      : util.kernel_exit,
        }

    def execute(self, user_command: list[str], command_set=None):
        
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

    def submit(self, user_command: list[str]):
        try:
            result = self.execute(n for n in user_command)
            self.global_settings.output_module.submit({"body": result})
        except KeyError as K:
            self.global_settings.output_module.submit({"body": "Commmand '%s' not recognised..." % (K.args[0])})

        except StopIteration as S:
            result = self.execute(n for n in user_command + ["help"])
            self.global_settings.output_module.submit({"body": result})

    @staticmethod
    def test(s: list[str]) -> list[str]:
        return s

    @staticmethod
    def help(s: list[str]) -> str:
        return "usage: <command> <args>\n\n\thelp: Display this help.\n\ttest: Returns provided arguments.\n\n\tquit/exit: Exit this program.\n"

    @staticmethod
    def helpSave(s: list[str]) -> str:
        # Unfinished. I'll do this later
        return "usage: save <module> <args>\n\n\tinput: Calls input save commands.\n\t\n"