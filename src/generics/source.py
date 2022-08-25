from generics import Generic
from abstract import Settings
from abc import abstractmethod
from typing import Tuple, List
from util import unimplemented


class SourceSettings(Settings):

    def __init__(self) -> None:
        self.ticker_list: List[str] = []
        self.api_key: str = ""
        self.period_length: str = ""

    def interperateSetting(self, key: str, value: str) -> Tuple[str, str]:
        return key, value

    @classmethod
    def validateLoadedConfig(self) -> None:
        unimplemented()


class Source(Generic):

    def __init__(self, global_settings: Settings) -> None:
        super().__init__(global_settings, None)


def load() -> None:
    unimplemented()


def list() -> None:
    unimplemented()
