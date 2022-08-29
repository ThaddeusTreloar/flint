
from abc import abstractmethod, ABC
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from termcolor import colored
from inspect import getmembers, isclass, isabstract
from generics import Generic
from typing import Optional, Any, Callable, Dict, Union, Tuple, List
from abstract import Settings
from tools import flatten
from tools import issubclassNoType, isinstanceNoType
from types import ModuleType
from importlib.machinery import SourceFileLoader


class HandlerSettings(Settings):

    '''
    Small settings for Handler child.
    Use as is or subclass by overriding self.interperateChildSettings
    '''

    @property
    def config_namespace(self) -> str:
        return self._config_namespace

    def __init__(self, config_path: Path, config_namespace: str):
        self._config_namespace: str = config_namespace
        self.enabled_modules: List[str] = []
        super().__init__(config_path)

    def interperateSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case "enabled_modules":
                return key, value.split(",")
            case _:
                return self.interperateChildSetting(key, value)

    def interperateChildSetting(self, key: str, value: str) -> Tuple[str, Any]:
        match key:
            case _:
                return key, value


class Handler(ABC):

    '''
    Parent class for all handler classes.
    Must implement:
        @property local_command_set(commands available for this modules), 
        @property module_type (the type of module it takes),
        @method start (signal from the kernel to load modules in and await instructions)
        @staticmethod help (returns help string)                print(value)
    After super().__init() you must:
        declare self._local_command_set if not None,

    The parent class will load all modules from the plugins directory for 
    the handler module type.
    These are accessible from self.available_module_tree
    The base command set automatically available to the handler is save in the __init__ function.
    '''

    @property
    @abstractmethod
    def module_type(self) -> Generic:
        '''
        Lets all parent functions know what modules the handler takes
        '''
        pass

    @property
    @abstractmethod
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        pass

    def __init__(self, settings: Any, parent_kernel: Any) -> None:  # settings: GlobalSettings
        self.parent_kernel = parent_kernel
        self.global_settings = settings
        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {
            "list": {
                "available": self.listAvailableModules,
                "commands": self.commands
            },
            "help": self.help,
            "module": {
                "enable": self.enable_module,
                "disable": self.disable_module,
            }
        }
        self.module_dir: Path = settings.plugins_dir.joinpath(
            self.module_type.plugins_dir_slug())
        self.available_module_tree: dict = self.build_module_tree()

        if self.parent_kernel is not None:
            self.addSelfToKernelCommandSet()

        if not bool(self.available_module_tree):
            # todo<0011>
            print(colored("!!No modules available for %s!!" %
                  (self.__class__), 'red'))

    @abstractmethod
    def start(self) -> None:
        '''
        MUST BE NON BLOCKINGfrom types import ModuleType
        This method is called when the kernel is ready to begin issuing instructions
        load any modules now.
        '''
        ...

    @abstractmethod
    def enable_module(self, module: str) -> None:
        '''
        Function to enable a module for the handler
        '''
        ...

    @abstractmethod
    def disable_module(self, module: str) -> None:
        '''
        Function to disable a module for the handler
        '''
        ...

    def build_module_tree(self) -> Dict[str, Union[Dict, Callable]]:

        module_tree = {}

        if self.module_dir.exists() and self.module_dir.is_dir():
            # Exclude pycache directories
            for child in (x for x in self.module_dir.iterdir() if not x.name.__contains__("pycache")):
                if child.is_dir():

                    if (child / Path("__init__.py")).exists():
                        module_path: str = str(child / Path('__init__.py'))

                        module: ModuleType = SourceFileLoader(
                            child.stem, module_path).load_module()

                        for obj in getmembers(module, isclass):

                            name = obj[0]
                            module_class = obj[1]

                            if issubclassNoType(module_class, self.module_type) and not isabstract(module_class) and module_class != self.module_type:
                                module_tree[name] = module_class

                            elif isabstract(module_class) and module_class != self.module_type and issubclassNoType(module_class, self.module_type):
                                # todo<0011>: need to add logging here
                                if self.global_settings.debug:
                                    print('module <%s.%s> is either an abstract class or is has not implemented all abstract properties of parent class.\n' % (
                                        module_class.__module__, name))

                            continue

            return module_tree

        else:

            # todo: Raise error/use default directory
            return {}

    def listAvailableModules(self) -> str:
        response = "Module Name\tDescription:\n\n"
        for k, v in self.available_module_tree.items():
            response += "%s\t%s\n" % (k, v.description.fget(v))

        return response

    def addChildCommandSet(self, child: Generic) -> None:

        if isinstanceNoType(child, self.module_type):
            self._local_command_set[child.__class__.__name__.lower(
            )] = child.local_command_set

    def removeChildCommandSet(self, child_name: str) -> None:

        child = self.available_module_tree[child_name]
        child_key_ref = child_name.lower()

        if child_key_ref in self._local_command_set:
            self._local_command_set.pop(child_key_ref)

    def addSelfToKernelCommandSet(self):
        self.parent_kernel.appendCommandSet(
            self.module_type.plugins_dir_slug())

    def rebuildCompletionCommandTree(self) -> None:
        '''
        Propogated to kernel
        '''
        self.parent_kernel.rebuildCompletionCommandTree()

    def buildCommand(self, branch) -> List[str]:
        commands = []
        for key, value in branch.items():
            if callable(value):
                commands.append(key)
            elif isinstance(value, Dict):
                commands.append([key+" "+x for x in self.buildCommand(value)])

        commands = flatten(commands)

        return commands

    def commands(self) -> str:
        # todo: Replace with util help generation
        buffer = "%s comands:\n\n" % (
            self.local_settings.config_namespace.capitalize())
        commands = self.buildCommand(self.local_command_set)

        buffer += "\n".join(commands)

        return buffer

    @staticmethod
    @abstractmethod
    def help() -> str:
        return "Todo"
