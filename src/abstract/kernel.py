from result import Err
from generics import Generic
from abc import abstractmethod, ABC
from pathlib import Path
from . import Settings
from typing import Tuple, Any, Dict
from queue import Queue
from threading import Lock
from result import Result, Ok, Err


class KernelSettings(Settings):

    @property
    def config_namespace(self) -> str:
        return "kernel"

    def __init__(self, config_path: Path) -> None:
        self.daemoniseCallingThread = False
        super().__init__(config_path)

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "daemonise":
                return "daemoniseThread", self.boolFromString(value)
            case _:
                return key, value


class Kernel(ABC):

    @property
    @abstractmethod
    def thread_queue(self) -> Queue:
        pass

    def __init__(self, global_settings: Settings) -> None:
        self.local_settings = KernelSettings(global_settings.config_path)
        self.global_settings = global_settings
        self.thread_locks: Dict[str, Lock] = {
            "print_lock": Lock()
        }
        self.command_queue: Queue = Queue()

    @abstractmethod
    def execute(self) -> None:
        '''
        Kernel api call to execute commands.
        Allows the kernel to control what commands are callable by input methods.
        '''

    @abstractmethod
    def start(self) -> None:
        '''
        Entry point for the kernel to start.
        '''

    def getLock(self, name) -> Result[Lock, None]:
        if name in self.thread_locks:
            return Ok(self.thread_locks[name])
        else:
            return Err(None)

    def getCommandQueue(self) -> Result[Queue, None]:
        if hasattr(self, "command_queue"):
            return Ok(self.command_queue)
        else:
            return Err(None)
