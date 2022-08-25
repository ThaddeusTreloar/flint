from abc import ABC, abstractmethod
from abstract import Settings
from abstract import Handler
from queue import Queue

class Generic(ABC):

    '''
    Abstract Class that is the parent for all generic modules.
    This is mainly used for type checking.

    All subclasses must call call 'super().__init__()' in their constructor.
    '''
    @property
    def thread_queue(self) -> Queue:
        pass

    @property
    @abstractmethod
    def daemoniseThread(self) -> bool:
        pass

    @property
    @abstractmethod
    def description(self):
        pass
    
    def __init__(self, global_settings: Settings, parent_handler: Handler=None):
        self.parent_handler: Handler = parent_handler
        self.global_settings: Settings = global_settings

    @property
    @abstractmethod
    def local_command_set(self) -> dict[str, object]:
        '''
        Function that returns the module level command set for the kernel
        command, 'save'.
        Must have the @property decorator.
        '''

    @abstractmethod
    def help(self, args: str) -> str:
        '''
        Help diaglogue called by kernel
        '''

    def rebuildCompletionCommandTree(self):
        self.parent_handler.rebuildCompletionCommandTree()

    def __eq__(self, other):
        if self.__class__ == other.__class__:
            return True

        else:
            return False
