from handlers import *
from abstract import Kernel
from abstract import Settings
from inspect import signature
from util import helpDialogue, kernel_exit
from typing import Iterator
from error import ModuleError
from termcolor import colored
from typing import Optional
from handlers import InputHandler, OutputHandler, PreProcessHandler, SourceHandler


class CoreKernel(Kernel):

    @property
    def daemoniseThread(self) -> bool:
        return self.local_settings.daemoniseThread

    @property
    def description(self) -> str:
        return 'The inbuilt core kernel.'

    def __init__(self, global_settings: Settings):

        super().__init__(global_settings)

        # Find some way to only have to enter
        self.local_command_set_: dict = {
            "test": self.test,
            "help": self.help,
            "exit": kernel_exit,
            "quit": kernel_exit,
        }

        self.input_handler = InputHandler(self.global_settings, self)
        self.output_handler = OutputHandler(self.global_settings, self)
        self.preprocess_handler = PreProcessHandler(
            self.global_settings, self)
        self.source_handler = SourceHandler(self.global_settings, self)

        self.rebuildCompletionCommandTree()

    @property
    def local_command_set(self) -> dict:
        return self.local_command_set_

    # <todo>: This is here to make the command set a bit more dynamic.
    # It is not necesarry at the moment but may be in future.
    def handlerLookup(self, handler: str) -> Optional[dict]:
        match handler:
            case "input":
                return self.input_handler.local_command_set
            case "output":
                return self.output_handler.local_command_set
            case "preprocess":
                return self.preprocess_handler.local_command_set
            case _:
                return None

    # todo: We may consider replacing this function with one
    # that descends a tree pre built during __init__
    # The only problem is that we would have to either
    # ditch hotswapping or build a messaging system that alerts the
    # kernel that swap has ocurred and the tree needs to be rebuilt.
    # <later> Actually... if everything is a pointer we could just
    # build the tree with pointers to each module.
    def execute(self, user_command: list[str]) -> str:

        command_set = self.local_command_set

        # Used to breaking pointer to parent function's list
        user_command = [n for n in user_command]

        for index, item in enumerate(user_command):

            if command_set.__contains__(item):

                if callable(command_set[item]):

                    if command_set[item] == self.handlerLookup:

                        command_set = command_set[item](item)
                        if command_set is None:
                            return "Commmand '%s' not recognised. Specifically the term '%s'..." % (" ".join(user_command), item)
                            # This works in conjunction with the handlerLookup function.
                            # Again, may be used in future.
                            #user_command.insert(index+1, user_command[index-1])

                    else:

                        if len(user_command[index+1:]) < 1:

                            if len(signature(command_set[item]).parameters) < 1:

                                return command_set[item]()

                            else:

                                break

                        else:
                            return command_set[item](user_command[index+1:])

                else:
                    command_set = command_set[item]
            else:
                return "Commmand '%s' not recognised. Specifically the term '%s'..." % (" ".join(user_command), item)

        raise StopIteration(1)

    def buildCompletionCommandTree(self, current_branch: dict) -> dict:

        tree = {}

        for key, value in current_branch.items():

            if callable(value) and value == self.handlerLookup:
                handler = self.handlerLookup(key)
                if handler is not None:
                    tree[key] = self.buildCompletionCommandTree(
                        handler)
                else:
                    tree[key] = {}
            elif callable(value):
                tree[key] = {}
            else:
                tree[key] = self.buildCompletionCommandTree(value)

        return tree

    def start(self):
        self.output_handler.start()
        self.output_handler.submit(
            {"body": "Welcome...\n\nType help for commands.\n"})
        self.input_handler.start()
        # todo: This is the main thread will exit without blocking.
        # As such any daemonised threads will stop here.
        # We need to add some sort of blocking so that the program
        # isn't kept alive by non-main threads.
        # Instead, the kernel should be in charge of when to
        # maintain the process or terminate it.

    def submit(self, user_command: list[str]):

        for r in range(user_command.count("")):
            user_command.remove("")

        try:
            result = self.execute(user_command)
            self.output_handler.submit({"body": result})

        except StopIteration as S:
            try:
                result = self.execute(user_command + ["help"])
                self.output_handler.submit({"body": result})
            except KeyError as K:
                # todo<0011>
                self.output_handler.submit(
                    {"body": "Insufficent arguments for command: No help command provided...\n"})
            except StopIteration as S:
                # todo<0011>
                self.output_handler.submit({"body": colored(
                    "Insufficent arguments for command and help command: Module not adhearing to command_set guidlines...\n", 'red')})

        except ModuleError as M:
            # Wtf is this here for?
            print(colored(
                "!!Module error triggered in command set. Let Thaddeus know. Don't know what this is for...!!", 'red'))
            self.output_handler.submit({"body": M.message})

    # todo: Currently does not propogate.

    def rebuildCompletionCommandTree(self):
        self.completionCommandTree = self.buildCompletionCommandTree(
            self.local_command_set)
        self.input_handler.newCompletionTree(self.completionCommandTree)

    def appendCommandSet(self, key: str):
        self.local_command_set[key] = self.handlerLookup

    @staticmethod
    def test(s: list[str]) -> list[str]:
        return s

    @staticmethod
    def help() -> str:
        return "usage: <command> <args>\n\n\thelp: Display this help.\n\ttest: Returns provided arguments.\n\n\tquit/exit: Exit this program.\n"

    @staticmethod
    def helpSave() -> str:
        # Unfinished. I'll do this later
        return helpDialogue(["usage: save <module> <args>", "", "<module>: Calls <module> 'save' kernel commands."])
