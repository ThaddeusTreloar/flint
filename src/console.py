import util
import indicator
import engine
import error

def buildTerminalPreamble(settings):

    buffer = "alchemist-sieve "

    if settings.TICKER:
        buffer += ":: " + settings.TICKER + " "

    buffer += ">> "

    return input(buffer)

def openConsole(settings):

    while True:
        user_command = (n for n in (buildTerminalPreamble(settings)).split(" "))
        status, err = execute_command(user_command, settings, command_set)

        if not status:
            pass
