from abstract.handler import Handler
from generics.input import Input
from pathlib import Path
from abstract.handler import HandlerSettings
from threading import Thread
from queue import Queue
from typing import List, Dict, Any, Union, Callable, Tuple


class InputSettings(HandlerSettings):

    def __init__(self, config_path=None):

        super().__init__(config_path, "input")

    def interperateChildSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case _:
                return key, value


class InputHandler(Handler):

    @property
    def module_type(self):
        return Input

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._local_command_set

    def __init__(self, settings, parent_kernel, completionCommandTree: dict = None):
        super().__init__(settings, parent_kernel)
        self.local_settings = InputSettings(self.global_settings.config_path)

        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "list": {
                "available": self.listAvailableModules,
                "active": self.listActiveInputs,
                "commands": self.commands
            },
            "help": self.help,
        }

        self.local_thread_queue: Queue = Queue()

        if completionCommandTree is not None:
            self.completionCommandTree: dict = completionCommandTree
        else:
            self.completionCommandTree = {}

        self.enabled_inputs: List[Input] = []
        self.active_inputs: List[Input] = []

        # Move this to parent class?
        self.started: bool = False

    def start(self):
        # todo<0011>: add feedback/logging
        for module in self.local_settings.enabled_modules:
            self.enable_input(module)

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

    def activate_input(self, module: Input):

        args = [self.global_settings, self]
        if module.completes:
            args.append(self.completionCommandTree)
            args.append(self.local_thread_queue)

        module = module(*args)

        module_thread = Thread(target=module.start)

        module_thread.name = "Input:%s" % (module.__class__.__name__)
        module_thread.daemon = module.daemoniseThread
        self
        return module_thread

    def enable_and_activate_input(self, module: str):
        pass

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
