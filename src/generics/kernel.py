from abc import abstractmethod
from settings import SettingsObject

class Kernel:

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        '''
        Kernel api call to execute commands.
        Allows the kernel to control what commands are callable by input methods.
        '''

    @abstractmethod
    def start(self, settings: SettingsObject):
        '''
        Entry point for the kernel to start.
        '''
