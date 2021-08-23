import error
import settings
from generics.kernel import Kernel

class CoreKernel(Kernel):

    def __init__(self):
        self.command_set: dict = {
        "set"       : {
            "ticker"    : settings.set_ticker,
            "interval"  : settings.setInterval,
        },
        "get"       : {
            "series"    : None
        },
        "load"      : {
            "source"    : source.load,
            "engine"    : engine.load,
        },
        "list"      : {
            "sources"    : source.list,
            "engines"    : engine.list,
        },
        "exit"      : util.console_exit,
        "quit"      : util.console_exit,
    }

    def execute(self, user_command: dict, settings: settings.SettingsObject, command_set=None) -> (bool, Exception):

        if command_set is None:
            command_set = self.command_set

        try:
            current_item = self.command_set[next(user_command)]

            if callable(current_item):
                return current_item([n for n in user_command], settings)
            else:
                return self.execute(user_command, settings, current_item)
    #'''
        except KeyError as K:
            print("Command %s not found" % (K))
            return False, K

        except StopIteration as S:
            print("Insufficient arguments")
            return False, S

        except error.InsufficientArgumentsError as I:
            print(I.msg)
            return False, I
    '''
        except Exception as E:
            util.panic(E)    
    '''

