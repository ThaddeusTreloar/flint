from inspect import isabstract
from pandas import DataFrame
from result import Err, Ok, OkErr, Result
from abstract import Handler, HandlerSettings
from typing import Any, Optional, Dict, Union, Callable, Tuple, List
from pathlib import Path
from generics import Generic, Source
from generics.actor import Actor
from generics.producer import Producer
from inbuilt_plugins.source.source_cache.source_cache import SourceCache


class SourceSettings(HandlerSettings):

    def __init__(self, config_path: Path) -> None:
        self.cache_data: bool = True
        self.cache_module: str = "SourceCache"

        super().__init__(config_path, "source")

    def interperateChildSetting(self, key, value) -> Tuple[str, Any]:
        match key:
            case "cache_data":
                return key, self.boolFromString(value, True)
            case "cache_module":
                return key, value
            case _:
                return key, value


class SourceHandler(Handler):

    '''
    Handler for managing source modules.
    todo: decide whether multiple source modules should be enabled
    '''

    @property
    def module_type(self):
        return Source

    @property
    def subclass_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return {
            "active_cache": self.active_cache_module,
            "request": self.submit
        }

    @property
    def module_command_sets(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._module_command_sets

    def active_cache_module(self) -> str:
        return self.local_settings.cache_module

    def __init__(self, settings: Any, parent_kernel: Any):
        self._module_command_sets: Dict[str, Union[str, Callable, Dict]] = {}

        super().__init__(settings, parent_kernel)

        self.local_settings: SourceSettings = SourceSettings(
            self.global_settings.config_path)

        match self.importModule(SourceCache, "SourceCache"):
            case Ok(module):
                self.available_module_tree['SourceCache'] = module
            case Err(e):
                if e != "nolog" and self.global_settings.debug:
                    print(e)
                self.local_settings.cache_module = "None"

        if not self.local_settings.cache_module in self.available_module_tree and "SourceCache" in self.available_module_tree:
            self.local_settings.cache_module = "SourceCache"

        self.cache: Source

    def addChildCommandSet(self, child: Generic) -> Result[str, str]:
        if isabstract(child):
            return Err("todo")
        else:
            self._module_command_sets[child.__class__.__name__.lower(
            )] = child.local_command_set
            return Ok("todo")

    def start(self) -> None:
        '''
        Setup cache and then enable the source module set in settings.
        '''
        if self.local_settings.cache_data:

            match self.enable_module(self.local_settings.cache_module):
                case Ok(module):
                    pass
                case Err(e):
                    # todo<0011>: Logging
                    print(e)

        for module in self.local_settings.enabled_modules:
            self.enable_module(module)

        # for module in self.enabled_modules:
           # self.enabled_sources.append(module(self.global_settings, self))

    def submit(self, module: str, function: str, **function_args) -> Result[Union[Dict, DataFrame], str]:
        if self.cache:
            match self.cache.requestData(function, **function_args):
                case Ok(data):
                    pass
                case Err(msg):
                    pass
        if module in self.module_command_sets:
            # self.module_command_sets[module]()
            pass

    @ staticmethod
    def help() -> str:
        return "todo"
