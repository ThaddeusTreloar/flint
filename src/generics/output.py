from generics.generic import Generic
from abc import abstractmethod
from abstract.settings import SettingsObject

class Output(Generic):

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    @property
    @abstractmethod
    def local_save_command_set():
        '''
        Function that returns the module level command set for the kernel
        command, 'save'.
        '''

    @classmethod
    @abstractmethod
    def submit(self, response: dict):
        '''
        Method for recieving output from the kernel.
        Dictionary format unfinished.
        '''