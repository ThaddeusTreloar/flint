from generics import Generic
from abc import abstractmethod
from abstract import Settings
from rlcompleter import Completer
from queue import Queue
from typing import Optional, Tuple, List, Dict, Any

import readline


class LocalCompleter(Completer):

    def __init__(self, tree: Dict) -> None:  # Dict[str, ...]
        self.namespace = tree
        super().__init__(tree)

    def complete(self, text: str, state: int) -> Optional[str]:
        """Return the next possible completion for 'text'.
        This is called successively with state == 0, 1, 2, ... until it
        returns None.  The completion should begin with 'text'.
        """

        if not text.strip():

            if state == 0:
                # Add Windows compatibility
                readline.insert_text('\t')
                readline.redisplay()
                return ''
            else:
                return None
        if state == 0:
            if " " in text:
                self.matches = self.ctx_matches(text)
            else:
                self.matches = self.global_matches(text)
        if self.matches is not None:
            return self.matches[state]
        else:
            return None

    def global_matches(self, text: str) -> List[str]:

        matches = []
        n = len(text)

        for nspace in [self.namespace]:
            for word, val in nspace.items():
                if word[:n] == text:
                    matches.append(word)

        if len(matches) == 1 and matches[0] == text:
            return self.ctx_matches(text)
        else:
            return matches

    def ctx_matches(self, text: str) -> List[str]:

        matches = []
        args: List[str] = text.split(" ")

        subject: str = args.pop()

        nspace = self.namespace

        for arg in args:

            if nspace.__contains__(arg):
                nspace = nspace[arg]
            else:

                return []

        n = len(subject)

        for word in nspace.keys():
            if word[:n] == subject:
                matches.append(" ".join(args+[word]))

        if len(matches) == 1 and matches[0] == text:
            return []
        else:
            return matches


class InputSettings(Settings):
    pass


class Input(Generic):

    '''
    Abstract Class for implementing input extensions.
    Core and default input extension is console.
    '''

    @staticmethod
    def plugins_dir_slug() -> str:
        return "input"

    @property
    def handler_thread_queue(self) -> Queue:
        return self._handler_thread_queue

    @property
    def kernel_thread_queue(self) -> Queue:
        return self._kernel_thread_queue

    @property
    @abstractmethod
    def local_command_set(self) -> dict:
        pass

    @property
    @abstractmethod
    def completes(self) -> bool:
        pass

    @property
    def completer(self) -> LocalCompleter:
        pass

    def __init__(self, global_settings: Settings, parent_handler: Any, handler_thread_queue: Queue):
        self._handler_thread_queue: Queue = handler_thread_queue
        super().__init__(global_settings, parent_handler)

    def submit(self, calling_module: str, user_command: list[str]) -> None:
        if self.parent_handler is not None:
            self.parent_handler.submit(calling_module, user_command)

    def checkAndActionQueue(self) -> Optional[str]:
        if self.handler_thread_queue:
            queue_item = self.handler_thread_queue.get(block=True)
            match queue_item:
                # todo: Can this all be moved to the input handler class
                # If the completer persists across all thread then this
                # needs to happen. Ah well, this is here if
                # needed in future anyways...
                case ("completion_tree", _):

                    if self.completes and self.parent_handler is not None:

                        while True:

                            match queue_item[1]:

                                case self.__class__.__name__:

                                    self.completer.namespace = self.parent_handler.completionCommandTree
                                    readline.set_completer(
                                        self.completer.complete)
                                    self.handler_thread_queue.task_done()
                                    break

                                case _:

                                    self.handler_thread_queue.put(queue_item)

                case ("continue", self.__class__.__name__):

                    self.handler_thread_queue.task_done()
                    return None

                case ("thread_exit", self.__class__.__name__):

                    self.handler_thread_queue.task_done()
                    return "exit"

    @abstractmethod
    def start(self) -> None:
        '''
        Entry point for input method
        '''
