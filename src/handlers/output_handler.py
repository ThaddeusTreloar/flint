from abstract.handler import Handler
from generics.output import Output
from pathlib import Path


class OutputHandler(Handler):

    @property
    def module_type(self):
        return Output

    @property
    def local_command_set(self) -> dict:
        return {
            "list": self.listAvailableModules,
            "help": self.help,
        }

    def __init__(self, settings, parent_kernel):
        super().__init__(settings, parent_kernel)

        self.enabled_outputs: [Output] = []
        self.active_outputs: [Output] = []

    def start(self):
        self.enable_output("Console")
        self.activate_output("Console")

    def enable_output(self, module: str):
        try:
            if not self.enabled_outputs.__contains__(self.availble_module_tree[module]):
                self.enabled_outputs.append(self.availble_module_tree[module])
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)

    def activate_output(self, module: str):
        try:
            if not self.active_outputs.__contains__(self.availble_module_tree[module]):
                self.active_outputs.append(
                    self.availble_module_tree[module](self.global_settings, self))
            return "<%s> enabled for %s handler" % (module, self.__class__)
        except KeyError as K:
            return "<%s> not available as a %s" % (module, self.__class__)

    def enable_and_activate_output(self, module: str):
        pass

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
