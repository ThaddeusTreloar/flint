from generics.generic import Generic
from abstract.settings import SettingsObject
from abc import abstractmethod

class MLNN(Generic):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    @classmethod
    @abstractmethod
    def train(self) -> None:
        '''
        ***Return type currently not known. Do not trust this return type.***
        Kernel-available call to train the module on provided data
        '''

    @classmethod
    @abstractmethod
    def predict(self, epoch: str=None) -> None:
        '''
        ***Return type currently not known. Do not trust this return type.***
        Kernel-available call to make predictions on provided data
        '''