from generics.generic import Generic
from abstract.settings import SettingsObject
from abc import abstractmethod

class Preprocess(Generic):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    def local_command_set(self) -> dict[str, object]:
        return {
            'calculate' : self.calculate,
            'inputs'    : self.listInputs
        }

    @abstractmethod
    def calculate(*args): # Return Type?
        '''
        This method is called when calculating a particular preprocessing method
        '''
        pass

    @abstractmethod
    def listInputs() -> str:
        '''
        This is used by the user to list both required and optional inputs
        '''
        pass
