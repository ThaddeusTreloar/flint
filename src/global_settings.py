# This will have to be cleaned up at some point
from abstract.settings import SettingsObject
from generics.input import Input
from generics.kernel import Kernel
from generics.output import Output
from generics.source import Source
from generics.generic import Generic
from generics.mlnn import MLNN
from generics.preprocess import Preprocess
from abstract.handler import Handler

from importlib import import_module, invalidate_caches
from pyclbr import readmodule
from inspect import getmembers, getmodule, isclass
from input import input_console
from output import output_console
from kernel import kernel_core
from source import yahoo_finance
from mlnn import svr
from pathlib import Path

import generics

class GlobalSettings(SettingsObject):

    def __init__(self):

        self.default_module_tree = {
            "input": input_console,
            "kernel": kernel_core,
            "mlnn": None,
            "output": output_console,
            "source": yahoo_finance,
        }

        # This is rediculous and will be phased out after the implementation of loadDefaultModule
        self.type_tree = {
            "input": Input,
            "kernel": Kernel,
            "output": Output,
            "source": Source,
        }


        self.filepath: str = "./config.yaml" # todo: 
        self.namespace: str = "global" # This is never referenced. What is it for?

        self.loadConfigFile(self.filepath, self.namespace)
        
        self.debug: bool = True

        self.plugins_dir:   Path = Path("./src")


        # todo: This is the tree that lists references to all available modules
        #self.available_module_tree

        self.input_module:  Input = self.loadDefaultModule("input")
        self.kernel_module: Kernel = self.loadDefaultModule("kernel")
        self.output_module: Output = self.loadDefaultModule("output")
        self.source_module: Source = self.loadDefaultModule("source")

        self.mlnn_module:   MLNN = None

        self.max_threads: int = 20

    
    # This method is deprecated as we are now using handler. This will not function for any 
    # future handler implementations. As we work handlers into all the generic modules, 
    # this will eventually be deleted. Loading of modules will be delegated directly to handlers.
    # todo: remove 

    def loadDefaultModule(self, module_parent: str) -> generics.generic.Generic:

        '''
        Generic function to load a default module. 
        '''

        module = self.default_module_tree[module_parent]

        # Iterate over all class members of the module
        for obj in getmembers(module, isclass):
            # If the class is both a subclass of 'Generic' and defined in the same module we
            # are searching then we can initialise it.
            if issubclass(obj[1], Generic) and getmodule(obj[1]) == module:
                return obj[1](self)

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

    def loadModule(self, path: str, module_parent: str, module_type: Generic) -> Generic:
        
        try:
            module = import_module("%s.%s" % (module_parent, path))
            invalidate_caches()
            # Iterate over all class members of the module
            for obj in getmembers(module, isclass):
                # If the class is both a subclass of 'Generic' and defined in the same module we
                # are searching then we can initialise it.
                if issubclass(obj[1], Generic) and getmodule(obj[1]) == module:
                    return self.validateObjectType( obj[1](self), module_type )

        except ModuleNotFoundError as error:
            # Handle this here error pls.
            raise ModuleNotFoundError(error)

        except TypeError as error:

            # Maybe make this generic? I went to do it briefly but it looked messy asf.
            if error.__str__() == 'Object not of useable type':

                incorrectModuleTypeFeedback( path, module_parent )
                return self.validateObjectType( _loadDefaultModule(module_parent), module_type )

            else:
                raise TypeError(error)

    def interperateSetting(self, key: str, value: str) -> object:
    
        return self.loadModule(value, key.split("_")[0], self.type_tree[key.split("_")[0]]) if key.__contains__("module") else value

    def validateLoadedConfig(): # Not completed
        
        """Do some Validation."""

        util.unimplemented()
    
    def hotSwapModule(path: str, module_parent: str, module_type: Generic):
        # loadModule()
        util.unimplemented()

    def hotSwapModuleBinary(module_parent: str, module_bin: Generic):

        util.unimplemented()
