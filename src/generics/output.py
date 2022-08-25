from generics import Generic
from abc import abstractmethod
from abstract import Settings

class Output(Generic):

    def __init__(self, global_settings: Settings, parent_handler):
        super().__init__(global_settings, parent_handler)

    @classmethod
    @abstractmethod
    def submit(self, response: dict):
        '''
        Method for recieving output from the kernel.
        Dictionary format unfinished.
        '''