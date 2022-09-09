from abc import ABC, abstractmethod
from pathlib import Path
from abstract import Settings
from queue import Queue
from typing import Optional, Any, Dict, Union, Callable, Type
from result import Ok, Err, Result
from tools import isinstanceNoType, issubclassNoType


class Generic(ABC):

    '''
    Abstract Class that is the parent for all generic modules.
    Must implement:
        property module_name (name of module)
        method help (This is delegated to children)
        method description (This is delegated to children)
        method plugins_dir_slug (location of modules)
    Parent class will:
        provide an equality function
    '''

    @property
    @abstractmethod
    def module_name(self) -> str:
        ...

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

    @abstractmethod
    def start(self) -> Result[str, str]:
        pass

    @staticmethod
    @abstractmethod
    def help() -> str:
        '''
        Returns help dialogue for module.
        '''
        ...

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

    def getModuleDirectoryConfig(self) -> Path:
        # Macro for returning a config path that points to the module's local directory
        return Path(Path(self.global_settings.plugins_dir) /
                    Path(self.plugins_dir_slug) /
                    Path(self.module_name) /
                    Path("config.yaml"))

    @abstractmethod
    def exit(self) -> None:
        '''
        This function is called by the parent handler when the module is disabled
        '''
