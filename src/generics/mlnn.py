from generics import Generic
from abstract import Settings
from abc import abstractmethod
from typing import Optional


class MLNN(Generic):

    def __init__(self, global_settings: Settings):
        super().__init__(global_settings)

    @classmethod
    @abstractmethod
    def train(self) -> None:
        '''
        ***Input/Return type currently not known. Do not trust.***
        Kernel-available call to train the module on provided data
        '''

    @classmethod
    @abstractmethod
    def predict(self, epoch: Optional[str] = None) -> None:
        '''
        ***Input/Return type currently not known. Do not trust.***
        Kernel-available call to make predictions on provided data
        '''
