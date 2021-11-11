from generics.input import Input
from abstract.settings import SettingsObject
from error import InsufficientArgumentsError

class ConsoleInput(Input):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    def start(self):

        while True:
            try:
                user_command = (n for n in (input()).split(" "))
                self.submit(user_command, self.global_settings)

            except KeyError as K:
                raise K

            except StopIteration as S:
                print("Insufficient arguments")

            except InsufficientArgumentsError as I:
                # Fix this
                print("Here")
