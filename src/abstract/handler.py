
from abc import abstractmethod, ABC
from pathlib import Path
from util import unimplemented
from importlib.util import spec_from_file_location, module_from_spec
from generics.generic import Generic

class Handler(ABC):
    
    @property
    @abstractmethod
    def module_dir(self):
        pass

    @property
    @abstractmethod
    def module_type(self):
        pass

    def __init__(self):

        self.module_tree: dict = self.build_module_tree()

    def build_module_tree(self):

        module_tree = {}

        if self.module_dir.exists() and self.module_dir.is_dir():
            for child in self.module_dir.iterdir():
                if child.is_dir():
                    # Retrieve from the directory, the spec from .py file of same name inside
                    if child.joinpath(child.name + '.py').exists():
                        spec = spec_from_file_location(child.name, child.joinpath(child.name + '.py'))
                        module = module_from_spec(spec)
                        spec.loader.exec_module(module)

                        try:
                            # Appending to module tree. Will append the class of childname inside the module
                            module_class = getattr(module, child.name)
                            
                            if issubclass(module_class, self.module_type):
                                module_tree[child.name] = module_class
                            else:
                                # todo<0011>: need to add logging here
                                print('module <%s> is not of type <%s>' % (child.name, self.module_type))
                                continue

                        except AttributeError:
                            # todo<0011>: need to add logging here
                            unimplemented()
                    else:
                        print("Module<%s> does not contain %s.py." % (child.name, child.name))
                        print("Either this isn't a <%s> module or the module is not built correctly." % (self.module_type.__name__))
                        print("Skipping...\n")
                        # todo<0011>: handle some logging

            return module_tree

        else:

            # todo: Raise error/use default directory
            unimplemented()