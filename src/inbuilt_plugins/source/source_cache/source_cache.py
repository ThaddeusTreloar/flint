from typing import Any, Callable, Dict, Tuple, Union

from result import Ok, Result
from abstract.settings import Settings
from generics import Source
from generics.actor import Actor
from generics.producer import Producer


class SourceCacheSettings(Settings):

    def config_namespace(self) -> str:
        return "cache"

    def __init__(self) -> None:
        self.cache_method: str = "sqlite3"
        # For infinite lifespan set to 0
        self.cache_lifespan: int = 0
        super().__init__()

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "cache_lifespan":
                return key, int(value)
            case _:
                key, value


class SourceCache(Source, Producer, Actor):

    @property
    def module_name(self) -> str:
        return "source_cache"

    @staticmethod
    def help() -> str:
        return "todo"

    @property
    def description(self) -> str:
        return "Caching module inbuilt to the SourceHandler"

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._local_command_set

    def __init__(self, global_settings: Any, parent_handler: Any) -> None:
        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "clear": self.clearCache,
            "help": self.help,
        }
        super().__init__(global_settings, parent_handler)

    def start(self) -> Result[str, str]:
        return Ok("Started...")

    def clearCache(self) -> None:
        ...

    def exit(self) -> None:
        pass
