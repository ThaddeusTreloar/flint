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

    def __init__(self, global_settings: SettingsObject):
        super().__init__(global_settings)

    @classmethod
    def submit(self, user_command: [str], settings: SettingsObject):
        # When this method is called from the subclass it won't be able to find
        # self.global_settings ???
        # Fix this later but for now it just takes the settings as an input...
        settings.kernel_module.submit(user_command)
    
    @classmethod
    @abstractmethod
    def start(self):
        '''
        Entry point for input method
        '''
