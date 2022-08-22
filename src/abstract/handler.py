
from abc import abstractmethod, ABC
from pathlib import Path
from util import unimplemented
from importlib.util import spec_from_file_location, module_from_spec
from termcolor import colored

class Handler(ABC):
    
    @property
    def module_dir(self) -> Path:
        return self._module_dir

    @property
    @abstractmethod
    def module_type(self):
        pass

    @property
    @abstractmethod
    def plugins_dir_slug(self) -> str:
        pass

    @property
    @abstractmethod
    def local_command_set(self) -> dict:
        pass

    def __init__(self, settings, parent_kernel):
        self.parent_kernel = parent_kernel
        self.global_settings = settings
        self._module_dir: Path = settings.plugins_dir.joinpath(self.plugins_dir_slug)
        self.availble_module_tree: dict = self.build_module_tree()

    def build_module_tree(self):

        module_tree = {}

        if self.module_dir.exists() and self.module_dir.is_dir():
            for child in (x for x in self.module_dir.iterdir() if not x.name.__contains__("pycache")):
                if child.is_dir():
                    # Retrieve from the directory, the spec from .py file of same name inside
                    # todo: Don't automatically load all modules. Check that they exist and then add to tree.
                    if child.joinpath(child.name + '.py').exists():
                        spec = spec_from_file_location(child.name, child.joinpath(child.name + '.py'))
                        module = module_from_spec(spec)
                        spec.loader.exec_module(module)

                        try:
                            # Appending to module tree. Will append the class of childname inside the module
                            module_class = getattr(module, child.name)
                            
                            if issubclass(module_class, self.module_type):
                                module_tree[child.name] = module_class

                                if self.global_settings.debug:
                                    # todo<0011>: need to add logging here
                                    print("Module <%s> loaded... to %s..\n" % (child.name, self.__class__))
                            else:
                                # todo<0011>: need to add logging here
                                print('module <%s> is not of type <%s>.\n' % (child.name, self.module_type))
                                continue

                        except AttributeError:
                            # todo<0011>: need to add logging here
                            print(colored("No class found in <%s.py> with name <%s>: Module potentially built incorrectly.\n" % (child.stem, child.stem), "red"))
                    else:
                        print(colored("Module<%s> does not contain %s.py." % (child.name, child.name), 'red'))
                        print(colored("Either this isn't a <%s> module or the module is not built correctly." % (self.module_type.__name__), 'red'))
                        print(colored("Skipping...\n", 'red'))
                        # todo<0011>: handle some logging
                elif child.is_file() and child.suffix == ".py":
                    # todo<0011>: 
                    print(colored("Loose python file <%s> in plugin dir: Module potentially built incorrectly.\n" % (child.name), "red"))
            return module_tree

        else:

            # todo: Raise error/use default directory
            unimplemented()

    def listAvailableModules(self):
        response = "Module Name\tDescription:\n\n"
        for k, v in self.availble_module_tree.items():
            response+="%s\t%s" % (k, v.description.fget(v))
        
        return response

    @abstractmethod
    def submit(self, r):
        pass