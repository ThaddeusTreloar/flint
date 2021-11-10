
from yaml import safe_load_all, safe_dump
from importlib import import_module, invalidate_caches
from typing import overload
from io import TextIOWrapper

from tools import Functor

from mlnn import svr
from generics.input import Input
from generics.kernel import Kernel
from generics.output import Output
from generics.source import Source
from generics.generic import Generic

from input import input_console
from output import output_console
from kernel import kernel_core
from source import yahoo_finance

import generics

class SettingsObject():
    
        mysql_host:    str = None
        mysql_user:    str = None
        mysql_db:      str = None
        yf_api_key:    str = None
        av_api_key:    str = None
        inst_range:    int = None
        predict_range: int = None
        interval_range:int = None
        ticker:        str = None
        interval_u:    str = None
        interval_n:    int = None

        plugins_dir:   str = None

        input_module:  Input = None
        kernel_module: Kernel = None
        output_module: Output = None
        source_module: Source = None

def incorrectModuleTypeFeedback(path: str, t: str):

    print("Object returned by 'returnInstance' in module %s is not of 'source' type" % (path))
    print("Loading default %s module..." % (t))

def validateObjectType(subject: Generic, T) -> Generic:

    if isinstance(subject, T):
        subject
    else:
        raise TypeError("Object not of useable type")

def loadDefaultModule(module_parent: str) -> generics.generic.Generic:

    default_tree = {
        "input": input_console,
        "kernel": kernel_core,
        "mlnn": None,
        "output": output_console,
        "preprocess": None,
        "source": yahoo_finance,
    }

    return default_tree[module_parent].returnInstance()

def loadModule(path: str, module_parent: str, module_type: Generic, settings: SettingsObject) -> Generic:
    
    try:
        module = import_module("%s.%s" % (module_parent, path))
        invalidate_caches()

        return validateObjectType( module.returnInstance(), module_type )

    except ModuleNotFoundError as error:
        # Handle this here error pls.
        raise ModuleNotFoundError(error)

    except TypeError as error:

        # Maybe make this generic? I went to do it briefly but it looked messy asf.
        if error.__str__() == 'Object not of useable type':

            incorrectModuleTypeFeedback( path, module_parent )
            return validateObjectType( loadDefaultModule(module_parent), module_type )

        else:
            raise TypeError(error)

# Just initialise this on object creation??
def setDefaults() -> SettingsObject:
    settings = SettingsObject()
    settings.mysql_host     = "localhost"
    settings.mysql_user     = "root"
    settings.mysql_db       = "alchemists-sieve"
    settings.av_api_key     = ""
    settings.yf_api_key     = ""
    settings.inst_range     = 0
    settings.predict_range  = 0
    settings.interval_range = 0
    settings.plugins_dir    = "./src"
    settings.input_module          = loadDefaultModule("input")
    settings.kernel_module         = loadDefaultModule("kernel")
    settings.output_module         = loadDefaultModule("output")
    return settings

def readInConfig(file_path: str) -> dict:
    
    try:
        with open(file_path, "r") as file:
            # Calling next directly on the loaded config may result in unpredictable behaviour
            raw = next(safe_load_all(file))
            # It might also be a good idea to reconsider this automatic selection of the 'config' tree.
            # Break up the config files maybe?
            return raw["config"]
    
    except FileNotFoundError as error:

        print("Config file not found, using default settings...")
        return None

def maskOverridenSettings(config: dict, settings: SettingsObject) -> SettingsObject:

    # Rework this to function in a for loop on the dict.
    if config:

        settings.mysql_host = config["MYSQL_HOST"]
        settings.mysql_user = config["MYSQL_USER"]
        settings.mysql_db = config["MYSQL_DB"]
        settings.av_api_key = config["AV_API_KEY"]
        settings.yf_api_key = config["YF_API_KEY"]
        settings.inst_range = config["INST_RANGE"]
        settings.predict_range = config["PREDICT_RANGE"]
        settings.interval_range = config["INTERVAL_RANGE"]
        # Fix this. Need some dependency management or something    
        # settings.plugins_dir = config["plugins_dir"]

        settings.input_module =  loadModule(config["input_module"], "input", Input, settings)
        settings.source_module = loadModule(config["source_module"], "source", Source, settings)
    
    return settings

def loadConfigFile(file_path: str) -> SettingsObject:

    return maskOverridenSettings(readInConfig(file_path), setDefaults())

def validateLoadedConfig(settings: SettingsObject) -> SettingsObject:
    
    """Do some Validation."""

    if not settings.input_module:
        settings.input_module = loadDefaultModule("input")

    if not settings.kernel_module:
        print(kernel_core.CoreKernel())
        settings.kernel_module = loadDefaultModule("kernel")

    return settings




