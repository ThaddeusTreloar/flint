
from abc import abstractmethod, ABC
from distutils.log import debug
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
from threading import Thread
from termcolor import colored
from inspect import getmembers, isclass, isabstract
from generics import Generic
from typing import Optional, Any, Callable, Dict, Type, Union, Tuple, List
from abstract import Settings
from tools import flatten
from tools import issubclassNoType, isinstanceNoType
from types import ModuleType
from importlib.machinery import SourceFileLoader
from result import Result, Err, Ok
from tools import recursiveDictionaryFold
from generics import *
from queue import Queue


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
        @property subclass_command_set(commands available for this modules),
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
        ...

    @property
    def local_command_set(self) -> Dict[str, Union[str, Callable, Dict]]:
        return self._local_command_set

    @property
    @abstractmethod
    def subclass_command_set(self) -> Optional[Dict[str, Union[str, Callable, Dict]]]:
        ...

    def __init__(self, settings: Any, parent_kernel: Any) -> None:  # settings: GlobalSettings
        self.parent_kernel = parent_kernel
        self.global_settings = settings
        inbuilt_command_set: Dict[str, Union[str, Callable, Dict]] = {
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
        if self.subclass_command_set is not None:
            self._local_command_set: Dict[str, Union[str, Callable, Dict]] = \
                recursiveDictionaryFold(
                    inbuilt_command_set, self.subclass_command_set)
        else:
            self._local_command_set = inbuilt_command_set

        self.module_dir: Path = settings.plugins_dir.joinpath(
            self.module_type.plugins_dir_slug())
        self.available_module_tree: dict = self.build_module_tree()

        if self.parent_kernel is not None:
            self.addSelfToKernelCommandSet()

        if not self.available_module_tree:
            # todo<0011>
            print(colored("!!No modules available for %s!!" %
                  (self.__class__), 'red'))

        self.active_module_queues: Dict[str, Queue] = {}
        self.active_modules: Dict[str, Union[Thread, Generic]] = {}

    @ abstractmethod
    def start(self) -> None:
        '''
        MUST BE NON BLOCKINGfrom types import ModuleType
        This method is called when the kernel is ready to begin issuing instructions
        load any modules now.
        '''
        ...

    def enable_module(self, name: str) -> str:

        match self.getAvailableModule(name):
            case Ok(module):
                match self.activate_module(module, name):
                    case Ok():
                        return f"Module<{name}> activated for {self.__class__.__name__} handler."
                    case Err(e):
                        return e
            case Err(e):
                # todo<0011>: logging
                return e

    def disable_module(self, module: str) -> str:

        match (self.getAvailableModule(module), self.getActiveModule(module)):

            case (Ok(c), Ok(m)):

                if c.classIsChild(Threader):
                    self.active_module_queues[module].put(QueueAction.Exit)
                    self.active_module_queues[module].join()
                    print("here")
                    del self.active_module_queues[module]
                else:
                    m.exit()

                del self.active_modules[module]

                self.removeChildCommandSet(module)

            case (Ok(), Err()):

                return f"Module<{module}> is not enabled."

            case (Err(), Err()):

                return f"Module<{module}> does not exist."

    def getAvailableModule(self, name) -> Result[Generic, str]:
        if name in self.available_module_tree:
            return Ok(self.available_module_tree[name])
        else:
            return Err(f"Module<{name}> not available to <{self.__class__.__name__}>.")

    def getActiveModule(self, name) -> Result[Union[Generic, Thread], str]:
        if name in self.active_modules:
            return Ok(self.active_modules[name])
        else:
            return Err(f"Module<{name}> not available to <{self.__class__.__name__}>.")

    def importModule(self, module_class: Type, name: str) -> Result[Type, str]:

        if issubclassNoType(module_class, self.module_type) \
            and not isabstract(module_class) \
                and module_class != self.module_type:
            return Ok(module_class)

        elif isabstract(module_class) and module_class != self.module_type \
                and issubclassNoType(module_class, self.module_type):
            # todo<0011>: need to add logging here
            if self.global_settings.debug:
                return Err('module <%s.%s> has not implemented all abstract properties of parent class.\n' % (
                    module_class.__module__, name))

        elif not issubclassNoType(module_class, self.module_type):
            return Err("nolog")

        # Add additional errors
        return Err("Module import failed: No information")

    def build_module_tree(self) -> Dict[str, Union[Dict, Callable]]:
        module_tree = {}
        plugin_dir = self.global_settings.plugins_dir
        if plugin_dir.exists() and plugin_dir.is_dir():
            for child in plugin_dir.rglob("__init__.py"):

                module: ModuleType = SourceFileLoader(
                    child.parent.stem, str(child)).load_module()

                for obj in getmembers(module, isclass):

                    name = obj[0]
                    module_class = obj[1]
                    # todo: use ==
                    match self.importModule(module_class, name):
                        case Ok(module):
                            module_tree[name] = module
                        case Err(e):
                            # todo<0011>: Do some logging
                            if e != "nolog" and self.global_settings.debug:
                                print(e)

                    continue

            return module_tree

        else:

            # todo: Raise error/use default directory
            return {}

    def initialiseModule(self, module: Generic, name: str) -> Result[Generic, str]:
        args = self.buildModuleArgs(module, name)

        try:
            m = module(**args)
            if module.classIsChild(Actor):
                self.addChildCommandSet(m)
            return Ok(m)
        except TypeError as e:
            return Err(f"Module {name} failed to initialise: {e}")

    def activate_module(self, module: Generic, name) -> Result[None, str]:

        match self.initialiseModule(module, name):

            case Ok(module):
                if isinstanceNoType(module, Threader):
                    module_thread = Thread(target=module.start)
                    module_thread.daemon = module.daemoniseThread
                    self.active_modules[name] = module_thread
                else:
                    self.active_modules[name] = module

                self.active_modules[name].start()

                if module.instanceIsChild(Actor):
                    self.addChildCommandSet(module)
                    self.rebuildCompletionCommandTree()

                return Ok()
            case Err(e):
                # todo: some Logging
                return Err(e)

    def listAvailableModules(self) -> str:
        response = "Module Name\tDescription:\n\n"
        for k, v in self.available_module_tree.items():
            response += "%s\t%s\n" % (k, v.description.fget(v))

        return response

    def addChildCommandSet(self, child: Generic) -> Result[str, str]:

        if isabstract(child):
            return Err("todo")
        else:
            self._local_command_set[child.__class__.__name__.lower(
            )] = child.local_command_set
            return Ok("todo")

    def removeChildCommandSet(self, child_name: str) -> None:

        if child_name.lower() in self._local_command_set:
            self._local_command_set.pop(child_name.lower())

        self.rebuildCompletionCommandTree()

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

    def buildModuleArgs(self, module: Generic, name: str) -> Dict[str, Any]:
        if not hasattr(self, "global_settings"):
            return Err(f"Module<{name} failed to initialise: Handler{self.__class__.__name__}\
                does not implement 'self.global_settings'>")
        args = {
            "global_settings": self.global_settings,
            "parent_handler": self
        }
        if module.classIsChild(Completable):
            if not hasattr(self, "completionCommandTree"):
                return Err(f"Module<{name} failed to initialise: Handler{self.__class__.__name__}\
                    does not implement 'self.completionCommandTree'>")
            args["tree"] = (self.completionCommandTree)
        if module.classIsChild(Threader):
            if not hasattr(self, "active_module_queues"):
                return Err(f"Module<{name} failed to initialise: Handler{self.__class__.__name__}\
                    does not implement 'self.active_module_queues'>")
            self.active_module_queues[name] = Queue()
            args["thread_queue"] = self.active_module_queues[name]
        if module.classIsChild(Printer):
            match self.parent_kernel.getLock("print_lock"):
                case Ok(lock):
                    args["print_lock"] = lock
                case Err():
                    return Err(f"Module<{name} failed to initialise: Parent kernel does not \
                        implement Kernel.thread_locks['print_lock']>")
        if module.classIsChild(Issuer):
            match self.parent_kernel.getCommandQueue():
                case Ok(q):
                    args["command_queue"] = q
                case Err():
                    return Err(f"Module<{name} failed to initialise: Parent kernel does not \
                        implement Kernel.command_queue>")
        return args

    @ staticmethod
    @ abstractmethod
    def help() -> str:
        return "Todo"
