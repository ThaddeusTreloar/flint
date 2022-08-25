from generics import Generic
from abc import abstractmethod
from abstract import Settings
from typing import Any


class Output(Generic):

    def __init__(self, global_settings: Settings, parent_handler: Any) -> None:
        super().__init__(global_settings, parent_handler)

    @classmethod
    @abstractmethod
    def submit(self, response: dict) -> None:
        '''
        Method for recieving output from the kernel.
        Dictionary format unfinished.
        '''
