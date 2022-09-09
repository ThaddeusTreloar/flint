from queue import Queue
from abc import ABC, abstractmethod
from threading import Thread, Lock
from typing import Optional, Type, List
from enum import Enum
from result import Ok, Err
import readline

from termcolor import colored


class QueueAction(Enum):
    Continue = 0
    CompletionTree = 1
    Output = 2
    Exit = 10


class Threaded(ABC):

    '''
    Abstract Trait class for modules that thread.
    Must implement:
        @property daemoniseThread (Whether the thread is dependant on the main thread.
            May end up being passed off to children of class)
        @property local_command_set (This is delegated to children)
    '''

    @property
    @abstractmethod
    def daemoniseThread(self) -> bool:
        ...

    @property
    def thread_queue(self) -> Queue:
        return self._thread_queue

    @property
    # @abstractmethod
    def thread_name(self) -> str:
        ...

    def __init__(self, thread_queue: Queue) -> None:
        self._thread_queue = thread_queue

    @abstractmethod
    def exit(self) -> None:
        '''
        Provides the threaded class to exit itself.
        Add cleanup here if needed otherwise just exit.
        '''
        ...

    def checkQueue(self) -> None:

        while not self.thread_queue.empty():
            item = self.thread_queue.get(block=True)
            match item:

                case (QueueAction.Output, output):
                    self.submit(output)
                    self.thread_queue.task_done()
                    continue

                case (QueueAction.CompletionTree, tree):
                    self.set_completer(tree)
                    self.thread_queue.task_done()
                    continue

                case (QueueAction.Exit):

                    self.thread_queue.task_done()

                    self.exit()

                case _:
                    if self.global_settings.debug:
                        # todo<0011>: some logging
                        print(
                            colored(f"!! Undefined queue action {item} for module <{self.__class__.__name__}>.", 'red'))

                    self.thread_queue.task_done()
