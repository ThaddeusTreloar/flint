from generics.input import Input
from settings import SettingsObject
from error import InsufficientArgumentsError

class ConsoleInput(Input):

    def __init__(self):
        pass

    def start(self, settings: SettingsObject):

        while True:
            try:
                user_command = (n for n in (build_terminal_preamble(settings)).split(" "))
                settings.kernel.execute(user_command, settings)

            except KeyError as K:
                raise K

            except StopIteration as S:
                print("Insufficient arguments")

            except InsufficientArgumentsError as I:
                print("Here")


def build_terminal_preamble(settings):

    buffer = "alchemist-sieve "

    if settings.TICKER:
        buffer += "(" + settings.TICKER + ") "

    buffer += ":: "

    return input(buffer)
