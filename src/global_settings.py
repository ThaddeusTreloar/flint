# This will have to be cleaned up at some point
import util

from abstract import Settings
from generics import Generic

from importlib import import_module, invalidate_caches
from pyclbr import readmodule
from inspect import getmembers, getmodule, isclass

from pathlib import Path
from pathlib import Path
from weakref import ref
from logging import warning, Logger, WARNING


class GlobalSettings(Settings):

    @property
    def config_namespace(self):
        return "global"

    def __init__(self):
        self.debug: bool = True
        self.plugins_dir:   Path = Path("./src/inbuilt_plugins")

        self.kernel_module = "CoreKernel"

        super().__init__()
        
        # todo: This is the tree that lists references to all available modules
        #self.available_module_tree

        self.max_threads: int = 20

    
    # This method is deprecated as we are now using handler. This will not function for any 
    # future handler implementations. As we work handlers into all the generic modules, 
    # this will eventually be deleted. Loading of modules will be delegated directly to handlers.
    # todo: remove 

    @staticmethod
    def incorrectModuleTypeFeedback(path: str, t: str):

        print("Object returned by 'returnInstance' in module %s is not of 'source' type" % (path))
        print("Loading default %s module..." % (t))

    @staticmethod
    def validateObjectType(subject: Generic, T) -> Generic:

        if isinstance(subject, T):
            return subject
        else:
            raise TypeError("Object not of useable type")

    def interperateSetting(self, key: str, value: str) -> object:
        match key:
            case "debug":
                return key, self.boolFromString(value)
            case _:
                return key, value

    def validateLoadedConfig(): # Not completed
        
        """Do some Validation."""

        util.unimplemented()
