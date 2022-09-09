from abc import ABC, abstractmethod
from abstract import Settings
from queue import Queue
from typing import Optional, Any, Dict, Union, Callable, Type
from result import Ok, Err, Result
from tools import isinstanceNoType, issubclassNoType


class Generic(ABC):

    '''
    Abstract Class that is the parent for all generic modules.
    Must implement:
        method help (This is delegated to children)
        method description (This is delegated to children)
    Parent class will:
        provide an equality function
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

    def __init__(self, global_settings: Settings, parent_handler: Any = None) -> None:
        self.parent_handler: Optional[Any] = parent_handler
        self.global_settings: Settings = global_settings

    @staticmethod
    @abstractmethod
    def help() -> str:
        '''
        Returns help dialogue for module.
        '''

    @staticmethod
    @abstractmethod
    def description() -> str:
        '''
        Returns description of module.
        '''
        ...

    def instanceIsChild(self, other) -> bool:
        if isinstanceNoType(self, other):
            return True

        else:
            return False

    @classmethod
    def classIsChild(cls, other) -> bool:
        if issubclassNoType(cls, other):
            return True

        else:
            return False

    @abstractmethod
    def exit(self) -> None:
        '''
        This function is called by the parent handler when the module is disabled
        '''
