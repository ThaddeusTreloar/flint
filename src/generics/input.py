from queue import Queue
from generics.issuer import Issuer
from .generic import Generic
from abc import abstractmethod
from abstract import Settings
from typing import Optional, Tuple, List, Dict, Any


class Input(Generic, Issuer):

    '''
    Abstract Class for implementing input extensions.
    Core and default input extension is console.
    '''

    @staticmethod
    def plugins_dir_slug() -> str:
        return "input"

    def __init__(self, global_settings: Settings, parent_handler: Any, command_queue: Queue):
        Generic.__init__(self, global_settings, parent_handler)
        Issuer.__init__(self, command_queue)

    @abstractmethod
    def start(self) -> None:
        '''
        Entry point for input method
        '''
