from generics import Generic
from abstract import Settings
from abc import abstractmethod


class Preprocess(Generic):

    @staticmethod
    def plugins_dir_slug() -> str:
        return "preprocess"

    def __init__(self) -> None:

        pass

    def local_command_set(self) -> dict[str, object]:
        return {
            'calculate': self.calculate,
            'inputs': self.listInputs,
        }

    @abstractmethod
    def calculate(*args) -> None:  # Return Type?
        '''
        This method is called when calculating a particular preprocessing method
        '''
        pass

    @abstractmethod
    def listInputs(self) -> str:
        '''
        This is used by the user to list both required and optional inputs
        '''
        pass
