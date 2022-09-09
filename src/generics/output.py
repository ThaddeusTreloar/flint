from generics import Generic
from abc import abstractmethod
from abstract import Settings
from typing import Any


class Output(Generic):

    @staticmethod
    def plugins_dir_slug() -> str:
        return "output"

    def __init__(self, global_settings: Settings, parent_handler: Any) -> None:
        super().__init__(global_settings, parent_handler)

    @abstractmethod
    def submit(self, response: dict) -> None:
        '''
        Method for recieving output from the kernel.
        Dictionary format unfinished.
        '''
