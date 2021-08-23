from abc import abstractmethod

class Input:

    '''
    Abstract Class for implementing input extensions.
    Core and default input extension is console.
    '''

    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        '''
        Entry point for input method
        '''