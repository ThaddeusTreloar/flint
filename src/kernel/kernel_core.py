import abstract.settings as s, util, error
from generics.kernel import Kernel
from error import InsufficientArgumentsError
from abstract.settings import SettingsObject

class CoreKernel(Kernel):

    def __init__(self, global_settings: SettingsObject):
        self.command_set: dict = {
            "exit"      : util.kernel_exit,
            "quit"      : util.kernel_exit,
        }
        
        super().__init__(global_settings)

    def execute(self, user_command: dict, settings, command_set=None):
        
        if not command_set:
            command_set = self.command_set

        try:
            current_item = command_set[next(user_command)]

            if callable(current_item):
                return current_item([n for n in user_command], settings)
            else:
                return self.execute(user_command, settings, current_item)

        except KeyError as K:
            raise K

        except StopIteration as S:
            raise S

        except InsufficientArgumentsError as I:
            raise I

    def start(self, settings):
        settings.input_module.start()
