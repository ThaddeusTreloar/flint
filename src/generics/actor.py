from abc import abstractmethod, ABC
from typing import Dict, Union, Callable


class Actor(ABC):

    '''
    Abstract Trait class for modules that take commands.
    Must implement:
        @property local_command_set (This is delegated to children)
    '''

    @property
    @abstractmethod
    # Dict[str, Union[str, Callable, ...]]
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        '''
        Function that returns the module level command set for the kernel.
        Must have the @property decorator.
        '''
