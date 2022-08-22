from abstract.handler import Handler
from generics.input import Input
from pathlib import Path

class InputHandler(Handler):

    @property
    def module_type(self):
        return Input

    @property
    def plugins_dir_slug(self) -> str:
        return "input"

    @property
    def local_command_set(self) -> dict:
        return {
            "list"  : self.listAvailableModules,
            "help"  : self.help,
        }

    def __init__(self, settings, parent_kernel):
        super().__init__(settings, parent_kernel)

        self.enabled_inputs: [Input] = []
        self.active_inputs: [Input] = []

        self.enable_input("Console")

    def start(self):
        self.activate_input("Console")

    def enable_input(self, module: str):
        try:
            if not self.enabled_inputs.__contains__(self.availble_module_tree[module]):
                self.enabled_inputs.append(self.availble_module_tree[module])
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)
        

    def activate_input(self, module: str):
        try:
            if not self.active_inputs.__contains__(self.availble_module_tree[module]):
                self.active_inputs.append(self.availble_module_tree[module](self.global_settings, self).start())
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)

    def enable_and_activate_input(self, module: str):
        pass

    def submit(self, user_command: list[str]):
        self.parent_kernel.submit(user_command)

    def help() -> str:
        return "Todo"
'''
    @classmethod
    def createSequence(self):
   '''     