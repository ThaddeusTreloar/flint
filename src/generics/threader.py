from queue import Queue
from abc import ABC, abstractmethod
from threading import Thread, Lock
from typing import Optional, Type, List
from enum import Enum
from result import Ok, Err
import readline


class QueueAction(Enum):
    Continue = 0
    CompletionTree = 1
    Output = 2
    Exit = 10


class Threader(ABC):

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

    def actionQueueItem(self, item: Type) -> None:

        match item:

            case (QueueAction.Output, output):
                self.submit(output)

            case (QueueAction.CompletionTree, tree):

                self.set_completer(tree)
                self.thread_queue.task_done()

            case (QueueAction.Exit):
                self.thread_queue.task_done()
                self.exit()

    def checkQueue(self) -> None:

        if self.thread_queue.empty():
            return
        else:
            item = self.thread_queue.get(block=False)
            self.actionQueueItem(item)
