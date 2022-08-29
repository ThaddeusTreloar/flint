from abstract.handler import Handler
from generics.input import Input
from pathlib import Path
from abstract.handler import HandlerSettings
from threading import Thread
from queue import Queue
from typing import List, Dict, Any, Union, Callable, Tuple, Optional
from tools import recursiveDictionaryFold

# This may be removed as potentially not needed anymore


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

        self._local_command_set = recursiveDictionaryFold(self._local_command_set, {
            "list": {
                "active": self.listActiveInputs,
            },
        })

        self.local_thread_queue: Queue = Queue()

        if completionCommandTree is not None:
            self.completionCommandTree: dict = completionCommandTree
        else:
            self.completionCommandTree = {}

        self.enabled_inputs: List[str] = []
        self.active_inputs: List[Thread] = []

        # Move this to parent class?
        self.started: bool = False

    def start(self):
        # todo<0011>: add feedback/logging
        for module in self.local_settings.enabled_modules:
            self.activate_input(self.enable_input(module))

        self.started = True

    def enable_module(self, module: str) -> str:
        if self.activate_input(self.enable_input(module)):
            return "Success"
        else:
            return "Failure"

    def disable_module(self, module: str) -> None:

        if module in self.available_module_tree and module in self.enabled_inputs:

            for active_input in self.active_inputs:

                if active_input.name.split(":")[1] == module:

                    # active_input._stop()
                    self.local_thread_queue.put(
                        ("thread_exit", module))

            self.local_thread_queue.join()

            self.removeChildCommandSet(module)

    def enable_input(self, module: str) -> Optional[Input]:

        if module in self.available_module_tree:
            if not module in self.enabled_inputs:
                self.enabled_inputs.append(module)
            return self.available_module_tree[module]
        else:
            return None

    def activate_input(self, module: Optional[Input]) -> bool:

        if module is None:
            return False
        else:

            args = [self.global_settings, self]
            args.append(self.local_thread_queue)
            if module.completes:
                args.append(self.completionCommandTree)

            module = module(*args)

            module_thread = Thread(target=module.start)

            module_thread.name = "Input:%s" % (module.__class__.__name__)
            module_thread.daemon = module.daemoniseThread

            self.active_inputs.append(module_thread)
            self.active_inputs[-1].start()
            return True

    def submit(self, calling_module: str, user_command: list[str]):
        self.parent_kernel.thread_queue.put((calling_module, user_command))

    def calling_module_continue(self, calling_module) -> None:
        self.local_thread_queue.put(("continue", calling_module))

    def listAvailableModules(self):
        # todo: Prettify
        return [x for x in self.available_module_tree.keys()]

    def listActiveInputs(self):
        # todo: Prettify
        return [x.__name__ for x in self.enabled_inputs]

    def newCompletionTree(self, tree):
        self.completionCommandTree = tree
        for obj in self.enabled_inputs:
            if self.available_module_tree[obj].completes:
                self.local_thread_queue.put(("completion_tree", obj))

    def exit(self):
        for module in self.enabled_inputs:
            self.disable_module(module)

    @ staticmethod
    def help() -> str:
        return "Todo"
