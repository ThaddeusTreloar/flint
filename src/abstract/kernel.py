import threading
from result import Err
from termcolor import colored
from generics import Generic
from abc import abstractmethod, ABC
from pathlib import Path
from handlers.input_handler import InputHandler
from handlers.output_handler import OutputHandler
from handlers.preprocess_handler import PreProcessHandler
from handlers.source_handler import SourceHandler

from util import kernel_exit
from . import Settings
from typing import Tuple, Any, Dict
from queue import Queue
from threading import Lock, Thread, current_thread
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
                return "daemoniseCallingThread", self.boolFromString(value)
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
        self.input_handler: InputHandler
        self.output_handler: OutputHandler
        self.preprocess_handler: PreProcessHandler
        self.source_handler: SourceHandler
        self.exit_permitted_modules: Dict[str,
                                          bool] = self.global_settings.exit_permitted_modules
        self.kernel_management_permitted_modules: Dict[str,
                                                       bool] = self.global_settings.kernel_management_permitted_modules

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

    def cleanup(self) -> None:
        self.input_handler.exit()
        kernel_exit()

    def exit(self) -> str:

        if current_thread().name not in self.exit_permitted_modules:
            # todo<0011>: logging
            return colored(f"Module <{current_thread().name}> not permitted to call kernel.exit().")

        cleanup_thread = Thread(target=self.cleanup)
        cleanup_thread.start()
        return "Exiting..."
