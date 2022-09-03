from threading import Thread
from numpy import isin
from abstract.handler import Handler, HandlerSettings
from generics.output import Output
from generics.threader import Threader
from pathlib import Path
from typing import List


class OutputHandler(Handler):

    @property
    def module_type(self):
        return Output

    @property
    def subclass_command_set(self) -> None:
        return None

    def __init__(self, settings, parent_kernel):
        super().__init__(settings, parent_kernel)
        self.local_settings = HandlerSettings(
            self.global_settings.config_path, "output")

        self.started: bool = False

    def start(self):
        for name in self.local_settings.enabled_modules:
            res = self.enable_module(name)
            if self.global_settings.debug:
                print(res)

        self.started = True

    def submit(self, user_command: dict):

        for name, module in self.active_modules.items():
            if isinstance(module, Thread):
                self.active_module_queues[name].put(user_command)
            else:

                module.submit(user_command)

    @staticmethod
    def help() -> str:
        return "Todo"


'''
    @classmethod
    def createSequence(self):
   '''
