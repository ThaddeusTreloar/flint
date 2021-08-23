import settings as s
import util
import indicator
import source
import engine
import error

def buildTerminalPreamble(settings):

    buffer = "alchemist-sieve "

    if settings.TICKER:
        buffer += ":: " + settings.TICKER + " "

    buffer += ">> "

    return input(buffer)

def execute_command(user_command, settings, command_set):

    try:
        current_item = command_set[next(user_command)]

        if callable(current_item):
            return current_item([n for n in user_command], settings)
        else:
            return execute_command(user_command, settings, current_item)
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

def openConsole(settings):

    command_set = {
        "set"       : {
            "ticker"    : s.setTicker,
            "indicator" : indicator.setIndicatorValue,
            "interval"  : s.setInterval,
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
            "indicators" : indicator.list
        },
        "engine"    : {
            settings.currentEngine.command_set
        },
        "exit"      : util.console_exit,
        "quit"      : util.console_exit,
    }

    while True:
        user_command = (n for n in (buildTerminalPreamble(settings)).split(" "))
        status, err = execute_command(user_command, settings, command_set)

        if not status:
            pass
