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

    @property
    def thread_queue(self) -> Optional[Queue]:
        return self._thread_queue

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

    def __init__(self, global_settings: Settings, parent_handler: Any, thread_queue: Optional[Queue] = None):
        self._thread_queue: Optional[Queue] = thread_queue
        super().__init__(global_settings, parent_handler)

    def submit(self, user_command: list[str]) -> None:
        # When this method is called from the subclass it won't be able to find
        # self.global_settings ???
        # Fix this later but for now it just takes the settings as an input...
        if self.parent_handler is not None:
            self.parent_handler.submit(user_command)

    def checkAndActionQueue(self) -> None:
        if self.thread_queue and not self.thread_queue.empty():

            queue_item = self.thread_queue.get(block=False)
            match queue_item:
                # todo: Can this all be moved to the input handler class
                # If the completer persists across all thread then this
                # needs to happen. Ah well, this is here if
                # needed in future anyways...
                case "completion_tree":
                    if self.completes and self.parent_handler is not None:
                        self.completer.namespace = self.parent_handler.completionCommandTree
                        readline.set_completer(self.completer.complete)

    @abstractmethod
    def start(self) -> None:
        '''
        Entry point for input method
        '''
