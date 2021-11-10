
from yaml import safe_load_all, safe_dump
from error import InsufficientArgumentsError, ConfigLoadError
from importlib import import_module, invalidate_caches
from typing import overload
from io import TextIOWrapper

from tools import Functor

from mlnn import svr
from generics.input import Input
from generics.kernel import Kernel
from generics.output import Output

from input import input_console
from output import output_console
from kernel import kernel_core

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


def loadDefaultInputModule() -> generics.input:
    return input_console.returnInstance()

def loadInput(path: str, settings: SettingsObject) -> generics.input:
    
    try:
        module = import_module("input." + path)
        invalidate_caches()

        module.returnInstance()

    except ModuleNotFoundError as error:
        raise ModuleNotFoundError(error)

def loadDefaultOutputModule() -> generics.output:
    return output_console.returnInstance()

def loadDefaultKernelModule() -> generics.kernel:
    return kernel_core.CoreKernel()

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
    settings.input_module          = loadDefaultInputModule()
    settings.kernel_module         = loadDefaultOutputModule()
    settings.output_module         = loadDefaultKernelModule()
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

    if config:

        settings.mysql_host = config["MYSQL_HOST"]
        settings.mysql_user = config["MYSQL_USER"]
        settings.mysql_db = config["MYSQL_DB"]
        settings.av_api_key = config["AV_API_KEY"]
        settings.yf_api_key = config["YF_API_KEY"]
        settings.inst_range = config["INST_RANGE"]
        settings.predict_range = config["PREDICT_RANGE"]
        settings.interval_range = config["INTERVAL_RANGE"]
        settings.data_engine = config["DATA_ENGINE"]
        # Fix this. Need some dependency management or something    
        # settings.plugins_dir = config["plugins_dir"]
        settings.input_module =  loadInput(config["input_module"], settings)
    
    return settings

def loadConfigFile(file_path: str) -> SettingsObject:

    return maskOverridenSettings(readInConfig(file_path), setDefaults())

def validateLoadedConfig(settings: SettingsObject) -> SettingsObject:
    
    """Do some Validation."""

    if not settings.input_module:
        settings.input_module = loadDefaultInputModule()

    if not settings.kernel_module:
        settings.kernel_module = loadDefaultKernelModule()

    return settings




