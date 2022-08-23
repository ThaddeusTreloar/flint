from abstract.settings import SettingsObject
from handlers.preprocess_handler import PreProcessHandler
from handlers.input_handler import InputHandler
from handlers.output_handler import OutputHandler
from generics.kernel import Kernel
from abstract.settings import SettingsObject
from itertools import chain
from inspect import signature
from util import helpDialogue, kernel_exit
from typing import Iterator
from error import ModuleError
from termcolor import colored
                
class CoreKernel(Kernel):

    @property
    def daemoniseCallingThread(self):
        return self.local_settings.daemoniseCallingThread

    @property
    def description(self):
        return 'The inbuilt core kernel.'

    def __init__(self, global_settings: SettingsObject):

        super().__init__(global_settings)
        
        self.input_handler = InputHandler(self.global_settings, self)
        self.output_handler = OutputHandler(self.global_settings, self)
        self.preprocess_handler: Preprocess = PreProcessHandler(self.global_settings, self)

        # Find some way to only have to enter
        self.local_command_set_: dict = {
            "input"     : self.handlerLookup,
            "preprocess" : self.handlerLookup,
            "test"      : self.test,
            "help"      : self.help,
            "exit"      : kernel_exit,
            "quit"      : kernel_exit,
        }

    @property
    def local_command_set(self) -> str:
        return self.local_command_set_
    
    # <todo>: This is here to make the command set a bit more dynamic. 
    # It is not necesarry at the moment but may be in future.
    def handlerLookup(self, handler: str):
        match handler:
            case "input":
                return self.input_handler.local_command_set
            case "output":
                return self.output_handler.local_command_set
            case "preprocess":
                return self.preprocess_handler.local_command_set
    
    def execute(self, user_command: list[str], command_set=None) -> str:
        
        if not command_set:
            command_set = self.local_command_set

        # Used to breaking pointer to parent function's list
        user_command = [n for n in user_command]

        for index, item in enumerate(user_command):
            
            if command_set.__contains__(item):
                
                if callable(command_set[item]):

                    if command_set[item] == self.handlerLookup:

                        command_set = command_set[item](item)
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

    def start(self):
        self.output_handler.submit({"body":"Welcome...\n\nType help for commands.\n"})
        self.input_handler.start()

    def submit(self, user_command: list[str]):
        try:
            result = self.execute(user_command)
            self.output_handler.submit({"body": result})

        except StopIteration as S:
            try:
                result = self.execute(user_command + ["help"])
                self.output_handler.submit({"body": result})
            except KeyError as K:
                # todo<0011>
                self.output_handler.submit({"body": "Insufficent arguments for command: No help command provided...\n"})
            except StopIteration as S:
                # todo<0011>
                self.output_handler.submit({"body": colored("Insufficent arguments for command and help command: Module not adhearing to command_set guidlines...\n", 'red')})

        except ModuleError as M:
            # Wtf is this here for?
            print(colored("!!Module error triggered in command set. Let Thaddeus know. Don't know what this is for...!!", 'red'))
            self.output_handler.submit({"body": M.message})

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