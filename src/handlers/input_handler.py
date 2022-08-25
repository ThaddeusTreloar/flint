from abstract.handler import Handler
from generics.input import Input
from pathlib import Path
from abstract.settings import Settings
from threading import Thread
from queue import Queue


class InputSettings(Settings):

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
        return self._local_command_set

    def __init__(self, settings, parent_kernel, completionCommandTree: dict = None):
        super().__init__(settings, parent_kernel)
        self.local_settings = InputSettings(self.global_settings.config_path)

        self._local_command_set: dict = {
            "list": {
                "available": self.listAvailableModules,
                "active": self.listActiveInputs,
            },
            "help": self.help,
        }

        self.local_thread_queue: Queue = Queue()

        self.completionCommandTree: dict = completionCommandTree

        self.enabled_inputs: [Input] = []
        self.active_inputs: [Input] = []

        self.enable_set_inputs()

        self.started: bool = False

    def start(self):
        # todo<0011>: add feedback/logging
        for module in self.enabled_inputs:

            module_thread = self.activate_input(module)
            self.active_inputs.append(module_thread)
            self.active_inputs[-1].start()

        self.started = True

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

        args = [self.global_settings, self]
        if module.completes:
            args.append(self.completionCommandTree)
            args.append(self.local_thread_queue)

        module = module(*args)
        # todo: I might move these two calls to the __init__ function of
        # genrics.generic.Generic. That way nobody will forget
        # to add this to anything.
        self.addChildCommandSet(module)

        self.rebuildCompletionCommandTree()

        module_thread = Thread(target=module.start)

        module_thread.name = "Input:%s" % (module.__class__.__name__)
        module_thread.daemon = module.daemoniseThread
        self
        return module_thread

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

    def newCompletionTree(self, tree):
        self.completionCommandTree = tree
        self.local_thread_queue.put(("completion_tree"))

    @staticmethod
    def help() -> str:
        return "Todo"


'''
    @classmethod
    def createSequence(self):
   '''
