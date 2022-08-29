from abstract.handler import Handler, HandlerSettings
from generics.output import Output
from pathlib import Path


class OutputHandler(Handler):

    @property
    def module_type(self):
        return Output

    @property
    def local_command_set(self) -> dict:
        return self._local_command_set

    def __init__(self, settings, parent_kernel):
        super().__init__(settings, parent_kernel)
        self.local_settings = HandlerSettings(
            self.global_settings.config_path, "output")

        self._local_command_set |= {}

        self.enabled_outputs: [Output] = []
        self.active_outputs: [Output] = []

    def start(self):
        for module in self.local_settings.enabled_modules:
            self.enable_output(module)
            self.activate_output(module)

    def enable_output(self, module: str):
        try:
            if not self.enabled_outputs.__contains__(self.available_module_tree[module]):
                self.enabled_outputs.append(self.available_module_tree[module])
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)

    def activate_output(self, module: str):
        try:
            if not self.active_outputs.__contains__(self.available_module_tree[module]):
                self.active_outputs.append(
                    self.available_module_tree[module](self.global_settings, self))
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)

    def enable_module(self, module: str) -> None:
        '''
        Function to enable a module for the handler
        '''
        ...

    def disable_module(self, module: str) -> None:
        '''
        Function to disable a module for the handler
        '''
        ...

    def submit(self, user_command: dict):
        for module in self.active_outputs:
            module.submit(user_command)

    @staticmethod
    def help() -> str:
        return "Todo"


'''
    @classmethod
    def createSequence(self):
   '''
