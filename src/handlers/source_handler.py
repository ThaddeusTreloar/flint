from abstract import Handler, HandlerSettings
from typing import Any, Optional, Dict, Union, Callable, Tuple, List
from pathlib import Path
from generics import Generic, Source


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


class sourceDatabase():

    def __init__(self) -> None:
        ...


class SourceCache(Source):

    @property
    def daemoniseThread(self) -> bool:
        return False

    @property
    def description(self) -> str:
        return "Caching module inbuilt to the SourceHandler"

    @property
    def threadable(self) -> bool:
        return True

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._local_command_set

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "clear": self.clearCache,
            "help": self.help,
        }
        super().__init__(global_settings, parent_handler)

    def clearCache(self) -> None:
        ...

    @staticmethod
    def help() -> str:
        return "todo"


class SourceHandler(Handler):

    '''
    Handler for managing source modules.
    todo: decide whether multiple source modules should be enabled
    '''

    @property
    def module_type(self):
        return Source

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._local_command_set

    def active_cache_module(self) -> str:
        return self.local_settings.cache_module

    def __init__(self, settings: Any, parent_kernel: Any):
        super().__init__(settings, parent_kernel)

        self.local_settings: SourceSettings = SourceSettings(
            self.global_settings.config_path)

        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "help": self.help,
            "active_cache": self.active_cache_module,
            "list": {
                "available": self.listAvailableModules,
                "commands": self.commands,
            },
            "module": {
                "enable": self.enable_module,
                "disable": self.disable_module,
            }
        }

        self.available_module_tree['SourceCache'] = SourceCache

        if not self.local_settings.cache_module in self.available_module_tree:
            self.local_settings.cache_module = "SourceCache"

        self.cache: Source
        self.enabled_sources: List[Source] = []

    def enable_module(self, module: str) -> None:
        # todo: check if already in enabled sources
        if module in self.available_module_tree:

            self.enabled_sources.append(self.available_module_tree[module](
                self.global_settings, self
            ))

        self.rebuildCompletionCommandTree()

    def disable_module(self, module: str) -> None:
        for source in self.enabled_sources:

            if isinstance(source, self.available_module_tree[module]):
                self.enabled_sources.remove(source)

        self.rebuildCompletionCommandTree()

    def start(self) -> None:
        '''
        Setup cache and then enable the source module set in settings.
        '''
        if self.local_settings.cache_data:
            self.cache = self.available_module_tree[self.local_settings.cache_module](
                self.global_settings, self
            )

        for module in self.local_settings.enabled_modules:
            self.enable_module(module)

        # for module in self.enabled_modules:
           # self.enabled_sources.append(module(self.global_settings, self))

    def submit(self) -> Any:  # todo: update this once class is complete
        ...

    @staticmethod
    def help() -> str:
        return "todo"
