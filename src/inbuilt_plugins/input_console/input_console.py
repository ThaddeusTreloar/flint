from threading import Lock
from queue import Queue
from threading import Thread

from click import command
from generics import Input, Completable, LocalCompleter, Actor, LocalCompleter
from abstract import Settings
from generics.issuer import Issuer
from generics.printer import Printer
from generics.threader import QueueAction, Threaded
from util import unimplemented
from tools import helpDialogue
import readline
from time import sleep


class Console(Input, Threaded, Completable, Actor, Printer):

    @property
    def module_name(self) -> str:
        return "input_console"

    @property
    def local_command_set(self) -> dict:
        return {
            "save": {
                "history": self.saveHistory,
                "help": self.saveHelp,
            },
        }

    @property
    def daemoniseThread(self):
        return False

    def __init__(self, global_settings: Settings, parent_handler, thread_queue: Queue, tree: dict, print_lock: Lock, command_queue: Queue):
        Input.__init__(self, global_settings, parent_handler, command_queue)
        Completable.__init__(self, tree)
        Threaded.__init__(self, thread_queue)
        Printer.__init__(self, print_lock)

    def getConsoleInput(self):
        self.print_lock.acquire()
        self.submit(input(self.build_terminal_preamble()).split(" "))
        self.print_lock.release()

    def start(self):

        while True:
            if self.thread_queue.empty:
                break
            else:
                self.checkQueue()

        while True:
            try:
                self.checkQueue()
                input_thread = Thread(target=self.getConsoleInput)
                input_thread.name = self.__class__.__name__
                input_thread.start()
                input_thread.join()

            except EOFError:
                break

    @staticmethod
    def build_terminal_preamble():

        buffer = "flint "

        buffer += ":: "

        return buffer

    @staticmethod
    def help() -> str:
        return helpDialogue(["available commands:", "", "save"])

    @staticmethod
    def description():
        return "Input module used for interacting with the kernel via a Command Line Interface."

    @staticmethod
    def saveHelp() -> str:
        return helpDialogue(["usage: save history <command> <args>", "", "history <path>: Save input history to <path>"])

    @staticmethod
    def exit() -> None:
        raise EOFError()

    def saveHistory(self, path: str) -> None:
        unimplemented()
