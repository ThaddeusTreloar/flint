from generics.generic import Generic
from abc import abstractmethod
from abstract.settings import SettingsObject

class InputSettings(SettingsObject):
    pass

class Input(Generic):

    '''
    Abstract Class for implementing input extensions.
    Core and default input extension is console.
    '''


    def __init__(self, global_settings: SettingsObject, parent_handler):
        super().__init__(global_settings, parent_handler)

    def submit(self, user_command: list[str]):
        # When this method is called from the subclass it won't be able to find
        # self.global_settings ???
        # Fix this later but for now it just takes the settings as an input...
        self.parent_handler.submit(user_command)

    @abstractmethod
    def start(self):
        '''
        Entry point for input method
        '''
