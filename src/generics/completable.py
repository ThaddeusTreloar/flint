from abc import abstractmethod, ABC
from rlcompleter import Completer
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


class Completable(ABC):

    '''
    Abstract Trait class for modules that need tab-completion.
    There is nothing to implement, just need to call Completable.__init__(someCompleterTree)
    '''

    @ property
    def completer(self) -> LocalCompleter:
        return self._completer

    def __init__(self, tree) -> None:
        self._completer = LocalCompleter(tree)
        readline.set_completer(self.completer.complete)
        readline.set_completer_delims("\n`~!@#$%^&*()-=+[{]}\|;:'\",<>/?")
        readline.parse_and_bind("tab: complete")

    def set_completer(self, tree) -> None:
        self.completer.namespace = tree
        readline.set_completer(
            self.completer.complete)
