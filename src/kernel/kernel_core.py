import settings as s, util, error
from generics.kernel import Kernel
from error import InsufficientArgumentsError

class CoreKernel(Kernel):

    def __init__(self):
        self.command_set: dict = {
            "set"       : {
                "ticker"    : s.set_ticker,
                "interval"  : s.set_interval,
            },
            "get"       : {
                "series"    : None
            },
            "load"      : {
                #"source"    : source.load,
                #"engine"    : engine.load,
            },
            "list"      : {
                # Need to find a place to store available options
                #"sources"    : sources.list,
                #"engines"    : engine.list,
            },
            "exit"      : util.kernel_exit,
            "quit"      : util.kernel_exit,
        }

    def execute(self, user_command: dict, settings: s.SettingsObject, command_set=None):
        
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

    def start(self, settings: s.SettingsObject):
        settings.input.start(settings)
