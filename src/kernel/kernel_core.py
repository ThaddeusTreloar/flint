import settings as s, util, error
from generics.kernel import Kernel
from error import InsufficientArgumentsError

def validateTickerCode(ticker_code):
    #return true if ticker valid otherwise false
    return True

def set_ticker(args, settings):

    if len(args) < 1 or not args[0]:
        raise InsufficientArgumentsError("set ticker requires 1 argument <ticker_code>")

    if validateTickerCode(args[0]):
        settings.ticker = args[0].upper()
        return True, None
    else:
        return False, None

def set_interval(args, settings):
    '''
    Set interval time frame for time series
    '''
    interval_n = ""
    interval_u = ""

    for char in args[0]:
        if char.isdigit():
            interval_n += char
        else:
            interval_u += char

    settings.interval_n = int(interval_n)
    settings.interval_u = interval_u

    return True, None

class CoreKernel(Kernel):

    def __init__(self):
        self.command_set: dict = {
            "set"       : {
                "ticker"    : set_ticker,
                "interval"  : set_interval,
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
        settings.input_module.start(settings)

def returnInstance() -> CoreKernel:
    return CoreKernel()