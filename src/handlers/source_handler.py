from abstract import Handler, Settings
from typing import Any, Optional, Dict, Union, Callable, Tuple
from pathlib import Path
from generics import Generic, Source


class SourceSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "source"

    def __init__(self, config_path: Optional[Path] = None) -> None:
        self.cache_data: bool = True
        self.cache_module: str = "SourceCache"
        super().__init__(config_path)

    def interperateSetting(self, key, value) -> Tuple[str, Any]:
        match key:
            case "cache_data":
                return key, self.boolFromString(value, True)
            case "cache_module":
                return key, value
            case _:
                return key, value


class SourceCache(Source):

    @property
    def daemoniseThread(self) -> bool:
        return False

    @property
    def description(self) -> str:
        return "Caching module inbuilt to the SourceHandler"

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return {
            "clear": self.clearCache,
        }

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
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

    def __init__(self, settings: Any, parent_kernel: Any):
        super().__init__(settings, parent_kernel)
        self.local_settings: SourceSettings = SourceSettings(
            self.global_settings.config_path)
        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "help": self.help,
        }
        self.availble_module_tree['cache'] = SourceCache
        if not self.availble_module_tree.__contains__(self.local_settings.cache_module):
            self.local_settings.cache_module = "SourceCache"
        self.cache: Source

    def start(self) -> None:
        '''
        Setup cache and then enable the source module set in settings.
        '''
        if self.local_settings.cache_data:
            self.cache = self.availble_module_tree[self.local_settings.cache_module](
                self.global_settings, self
            )

    def submit(self) -> Any:  # todo: update this once class is complete
        ...

    @staticmethod
    def help() -> str:
        return "todo"
