from abc import ABC, abstractmethod
from abstract.settings import SettingsObject

class Generic(ABC):

    '''
    Abstract Class that is the parent for all generic modules.
    This is mainly used for type checking.

    All subclasses must call call 'super().__init__()' in their constructor.
    '''

    @property
    @abstractmethod
    def description(self):
        pass
    
    def __init__(self, global_settings: SettingsObject):
        self.global_settings = global_settings