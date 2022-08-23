from abstract.handler import Handler
from generics.input import Input
from pathlib import Path
from abstract.settings import SettingsObject
from threading import Thread

class InputSettings(SettingsObject):

    @property
    def config_namespace(self):
        return "input"

    def __init__(self, config_path=None):
        self.enabled_inputs = ["Console"]
        super().__init__(config_path)

    def interperateSetting(self, key: str, value: str) -> object:
        match key:
            case "modules":
                return key, value.split(",")
            case _:
                return key, value

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
            "list"  : {
                "available" : self.listAvailableModules,
                "active" : self.listActiveInputs,
            },
            "help"  : self.help,
        }

    def __init__(self, settings, parent_kernel):
        super().__init__(settings, parent_kernel)
        self.local_settings = InputSettings(self.global_settings.config_path)

        self.enabled_inputs: [Input] = []
        self.active_inputs: [Input] = []

        self.enable_set_inputs()

    def start(self):

        for module in self.enabled_inputs:
            
            module = module(self.global_settings, self)
            
            module_thread = Thread(target=module.start)
            module_thread.setDaemon(True)

            self.active_inputs.append(module_thread)
            self.active_inputs[-1].start()

    def enable_input(self, module: str):
        if module in self.availble_module_tree:
            if not self.enabled_inputs.__contains__(self.availble_module_tree[module]):
                self.enabled_inputs.append(self.availble_module_tree[module])
            # todo<0011>
            return "<%s> enabled for %s handler" % (module, self.__class__)
        else:
            # todo<0011>
            return "<%s> not available as a %s" % (module, self.__class__)
        
    def activate_input(self, module: str):
        if module in self.availble_module_tree:
            #that will have to be redone
            if not self.active_inputs.__contains__(self.availble_module_tree[module]):
                self.active_inputs.append(self.availble_module_tree[module](self.global_settings, self).start())
            return "<%s> enabled for %s handler" % (module, self.__class__)
        else:
            return "<%s> not available as a %s" % (module, self.__class__)

    def enable_and_activate_input(self, module: str):
        pass

    def enable_set_inputs(self):
        for module in self.local_settings.enabled_inputs:
            self.enable_input(module)

    def submit(self, user_command: list[str]):
        self.parent_kernel.submit(user_command)

    def listAvailableModules(self):
        # todo: Prettify
        return [x for x in self.availble_module_tree.keys()]

    def listActiveInputs(self):
        # todo: Prettify
        return [x.__name__ for x in self.enabled_inputs]

    @staticmethod
    def help() -> str:
        return "Todo"
'''
    @classmethod
    def createSequence(self):
   '''     