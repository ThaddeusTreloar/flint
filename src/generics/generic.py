from abc import ABC, abstractmethod
from abstract import Settings
from queue import Queue
from typing import Optional, Any, Dict, Union, Callable


class Generic(ABC):

    '''
    Abstract Class that is the parent for all generic modules.
    Must implement:
        @property daemoniseThread (Whether the thread is dependant on the main thread.
            May end up being passed off to children of class)
        @property plugins_dir_slug (The directory in plugins_dir where plugins of this type can be found)
        @property local_command_set (This is delegated to children)
        method help (This is delegated to children)
    Parent class will:
        add it's own command set to the handler
        signal to the kernel to rebuild the completion tree for input modules
        provide an equality function
    After super().__init() you must:
        declare self._local_command_set if not None,
    '''
    @property
    def thread_queue(self) -> Optional[Queue]:
        pass

    @property
    @abstractmethod
    def daemoniseThread(self) -> bool:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    # Dict[str, Union[str, Callable, ...]]
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        '''
        Function that returns the module level command set for the kernel
        command, 'save'.
        Must have the @property decorator.
        '''

    @staticmethod
    @abstractmethod
    def plugins_dir_slug() -> str:
        '''
        Lets all parent functions know where to look in the plugin dir
        for modules. This must be a static callable as it is called
        on the uninitialised class rather than a class instance.
        '''
        pass

    def __init__(self, global_settings: Settings, parent_handler: Optional[Any] = None) -> None:
        self.parent_handler: Optional[Any] = parent_handler
        self.global_settings: Settings = global_settings
        if self.parent_handler is not None:
            self.parent_handler.addChildCommandSet(self)
            self.rebuildCompletionCommandTree()

    @staticmethod
    @abstractmethod
    def help() -> str:
        '''
        Help diaglogue called by kernel
        '''

    def rebuildCompletionCommandTree(self) -> None:
        '''
        Propogates back to kernel
        '''
        if self.parent_handler is not None:
            self.parent_handler.rebuildCompletionCommandTree()

    def __eq__(self, other: Any) -> bool:
        if self.__class__ == other.__class__:
            return True

        else:
            return False
