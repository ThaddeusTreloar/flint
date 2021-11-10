from generics.generic import Generic

from abc import abstractmethod

class Kernel(Generic):

    def __init__(self):
        pass

    @abstractmethod
    def execute(self):
        '''
        Kernel api call to execute commands.
        Allows the kernel to control what commands are callable by input methods.
        '''

    @abstractmethod
    def start(self, settings):
        '''
        Entry point for the kernel to start.
        '''
