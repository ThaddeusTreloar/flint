from generics.input import Input
from error import InsufficientArgumentsError

class ConsoleInput(Input):

    def __init__(self):
        pass

    def start(self, settings):

        while True:
            try:
                user_command = (n for n in (input(build_terminal_preamble(settings))).split(" "))
                settings.kernel_module.execute(user_command, settings)

            except KeyError as K:
                raise K

            except StopIteration as S:
                print("Insufficient arguments")

            except InsufficientArgumentsError as I:
                print("Here")

def build_terminal_preamble(settings):

    buffer = "alchemist-sieve "

    if settings.ticker:
        buffer += "(" + settings.ticker + ") "

    buffer += ":: "

    return buffer

def returnInstance() -> Input:
    return ConsoleInput()