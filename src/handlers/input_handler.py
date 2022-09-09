from operator import length_hint, mod
from readline import set_completer

from termcolor import colored
from abstract.handler import Handler
from generics import Input, Threaded, Completable, Actor, QueueAction
from pathlib import Path
from abstract.handler import HandlerSettings
from threading import Thread
from queue import Queue
from typing import List, Dict, Any, Union, Callable, Tuple, Optional

from result import Result, Ok, Err
from generics.issuer import Issuer
from generics.printer import Printer

from tools import isinstanceNoType
from util import panic


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
    def subclass_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return {
        }

    def __init__(self, settings, parent_kernel, completionCommandTree: dict = None):
        super().__init__(settings, parent_kernel)
        self.local_settings = InputSettings(self.global_settings.config_path)

        if completionCommandTree is not None:
            self.completionCommandTree: dict = completionCommandTree
        else:
            self.completionCommandTree = {}

        # Move this to parent class?
        self.started: bool = False

    def start(self) -> None:
        # todo<0011>: add feedback/logging
        for name in self.local_settings.enabled_modules:
            res = self.enable_module(name)
            if self.global_settings.debug:
                print(res)

        if len(self.active_modules) < 1:
            if len(self.available_module_tree) < 1:
                panic(colored(f"No input modules available. Cannot contine...", "red"))
            else:
                panic(
                    colored(f"No valid input modules enabled. Cannot contine...", "red"))

        self.started = True

    def somefunc(self, global_settings, parent_handler, thread_queue, tree: dict = None) -> None:
        print(global_settings)
        print(parent_handler)

    def submit(self, user_command: list[str]):
        self.parent_kernel.submit(user_command)

    def listActiveInputs(self):
        # todo: Prettify
        return [x.__name__ for x in self.active_modules.keys()]

    def newCompletionTree(self, tree) -> None:
        self.completionCommandTree = tree
        for name in self.active_modules.keys():
            if self.available_module_tree[name].classIsChild(Completable):
                if self.available_module_tree[name].classIsChild(Threaded):
                    self.active_module_queues[name].put(
                        (QueueAction.CompletionTree, tree))
                else:
                    match self.getActiveModule(name):
                        case Ok(module):
                            module.set_completer(tree)
                        case Err(e):
                            if self.global_settings.debug:
                                print(e)

    def exit(self):
        module_list = [x for x in self.active_modules.keys()]
        for module in module_list:
            self.disable_module(module)

    @ staticmethod
    def help() -> str:
        return "Todo"
