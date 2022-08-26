
from abc import abstractmethod, ABC
from pathlib import Path
from util import unimplemented
from importlib.util import spec_from_file_location, module_from_spec
from termcolor import colored
from inspect import getmembers, isclass, isabstract
from generics import Generic
from typing import Optional, Any, Callable, Dict, Union, no_type_check


# These two functions are necesarry as mypy will throw an error
# when passing dynamic types.
@no_type_check
def issubclassNoType(object: Any, class_: Any) -> bool:
    return issubclass(object, class_)


@no_type_check
def isinstanceNoType(object: Any, class_: Any) -> bool:
    return isinstance(object, class_)


class Handler(ABC):

    '''
    Parent class for all handler classes.
    Must implement:
        @property local_command_set(commands available for this modules), 
        @property module_type (the type of module it takes),
        @method start (signal from the kernel to load modules in and await instructions)
        @staticmethod help (returns help string)
    Parent class implies:
        plugin_dir_slug (from module_type), 
        availble_module_tree (from module_type)
    After super().__init() you must:
        declare self._local_command_set if not None,

    The parent class will load all modules from the plugins directory for 
    the handler module type.
    These are accessible from self.available_module_tree
    '''

    @property
    def module_dir(self) -> Path:
        return self._module_dir

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
        self._local_command_set: Dict[str, Union[str, Callable, Dict]] = {}
        self._module_dir: Path = settings.plugins_dir.joinpath(
            self.module_type.plugins_dir_slug())
        self.availble_module_tree: dict = self.build_module_tree()

        if self.parent_kernel is not None:
            self.addSelfToCommandSet()

        if not bool(self.availble_module_tree):
            # todo<0011>
            print(colored("!!No modules available for %s!!" %
                  (self.__class__), 'red'))

    @abstractmethod
    def start(self) -> None:
        '''
        This method is called when the kernel is ready to begin issuing instructions
        load any modules now.
        '''
        pass

    def build_module_tree(self) -> Dict[str, Union[Dict, Callable]]:

        module_tree = {}

        if self.module_dir.exists() and self.module_dir.is_dir():
            for child in (x for x in self.module_dir.iterdir() if not x.name.__contains__("pycache")):
                if child.is_dir():
                    # Retrieve from the directory, the spec from .py file of same name inside
                    # todo: Don't automatically load all modules. Check that they exist and then add to tree.
                    if child.joinpath(child.name + '.py').exists():
                        spec = spec_from_file_location(
                            child.name, child.joinpath(child.name + '.py'))
                        if spec is not None:
                            module = module_from_spec(spec)
                            loader = spec.loader
                            if loader is not None:
                                loader.exec_module(module)

                        try:
                            # Appending to module tree. Will append the class of childname inside the module

                            for obj in getmembers(module, isclass):

                                # todo: change this to append the name instead..
                                # Can be done by reworking the tree to be list of tuples or dictionary
                                # (name, path)
                                # That way modules aren't immediatly loaded in.
                                # todo: This will also pickup any abstract subclasses of Type(Generic) such
                                # as ApiSource(Source)

                                if issubclassNoType(obj[1], self.module_type) and not isabstract(obj[1]) and obj[1] != self.module_type:
                                    module_tree[obj[0]] = obj[1]

                                    if self.global_settings.debug:
                                        # todo<0011>: need to add logging here
                                        print("Module <%s> loaded... to %s..\n" % (
                                            obj[0], self.__class__))
                                else:
                                    if not issubclassNoType(obj[1], self.module_type):
                                        if self.global_settings.debug:
                                            print('module <%s> is not of type <%s>.\n' % (
                                                obj[0], self.module_type))
                                    elif isabstract(obj[1]) and obj[1] != self.module_type and issubclassNoType(obj[1], self.module_type):
                                        # todo<0011>: need to add logging here
                                        if global_settings.debug:
                                            print('module <%s.%s> is either an abstract class or is has not implemented all abstract properties of parent class.\n' % (
                                                obj[1].__module__, obj[0]))
                                    continue

                        except AttributeError:
                            # todo<0011>: need to add logging here
                            print(colored("No class found in <%s.py> with name <%s>: Module potentially built incorrectly.\n" % (
                                child.stem, child.stem), "red"))
                    else:
                        print(colored("Module<%s> does not contain %s.py." %
                              (child.name, child.name), 'red'))
                        print(colored("Either this isn't a <%s> module or the module is not built correctly." % (
                            self.module_type.__class__), 'red'))
                        print(colored("Skipping...\n", 'red'))
                        # todo<0011>: handle some logging
                elif child.is_file() and child.suffix == ".py":
                    # todo<0011>:
                    if self.global_settings.debug:
                        print(colored("Loose python file <%s> in plugin dir: Module potentially built incorrectly.\n" % (
                            child.name), "red"))
            return module_tree

        else:

            # todo: Raise error/use default directory
            return {}

    def listAvailableModules(self) -> str:
        response = "Module Name\tDescription:\n\n"
        for k, v in self.availble_module_tree.items():
            response += "%s\t%s" % (k, v.description.fget(v))

        return response

    def getMutableLocalCommandSet(self) -> Optional[Dict[str, Dict]]:
        if hasattr(self, "_local_command_set"):
            return self._local_command_set
        else:
            return None

    def addChildCommandSet(self, child: Generic) -> None:
        if isinstanceNoType(child, self.module_type):
            mutable_command_set: Optional[Dict] = self.getMutableLocalCommandSet(
            )
            if mutable_command_set is not None:
                mutable_command_set[child.__class__.__name__.lower(
                )] = child.local_command_set
            # todo: quietly fail?

    def addSelfToCommandSet(self):
        self.parent_kernel.appendCommandSet(
            self.module_type.plugins_dir_slug())

    def rebuildCompletionCommandTree(self) -> None:
        self.parent_kernel.rebuildCompletionCommandTree()

    @staticmethod
    @abstractmethod
    def help() -> str:
        return "Todo"
